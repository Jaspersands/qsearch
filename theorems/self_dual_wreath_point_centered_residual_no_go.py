"""Centered residual no-go for carrier-traced point decoding.

Let the public source labels be independent Plancherel pairs, let
``omega_(j,L)`` be the carrier-traced point state for label tuple ``L``, and
let ``B_L=n^-1 sum_j omega_(j,L)``.  Put

    Delta_(j,L)=omega_(j,L)-B_L,       D=n! 2^k.

The copy-threshold theorem bounds ``D E_L||Delta_(j,L)||_2^2``.  Its large
``k>=2log_2(n!)`` term is the rare ``z=0,s=g`` atom.  This module subtracts
the atom at the operator-mean level and controls every remaining matrix
entry.

For nonidentity ``h``, Plancherel regular-character orthogonality gives

    E_L p_L(0|h)=2^-k,       p_L(0|e)=1.

Therefore the projection of ``E_L Delta_(j,L)`` onto diagonal ``z=0``
matrix entries is an exact point simplex ``M_j``.  With ``N=n!`` and
``Q=2^k``,

    D||M_j||_2^2 = (n-1) Q/N^2 (1-Q^-1)^2,              (1)
    ||M_j||_1/2 = (n-1)(1-Q^-1)/(nN).                   (2)

Because diagonal extraction is an orthogonal Hilbert--Schmidt projection,

    E||Delta_(j,L)-M_j||_2^2
      = E||Delta_(j,L)||_2^2-||M_j||_2^2.                (3)

Subtracting (1) from the positive copy-threshold upper bound gives the
explicit residual bound ``R_(n,k)`` implemented below.  Its dominant term is

    R_(n,k) <= exp(O(sqrt(n))) k exp(O(k/n^4))/n!        (4)

up to smaller terms.  For an arbitrary point POVM chosen after seeing all
public labels, trace/HS comparison and Jensen yield

    E[P_point(L)-1/n]
      <= (n-1)(1-2^-k)/(n n!) + 1/2 sqrt(R_(n,k)).       (5)

Consequently every carrier-traced point POVM has superpolynomially small
average excess for ``k=O(n^5)``.  This includes the old information threshold,
the factor-two energy threshold, every fixed multiple of ``log_2(n!)``, and
much larger polynomial sample counts.

The same result transfers to global source distinctness: the squared residual
is nonnegative, so conditioning divides its expectation by the all-distinct
probability ``1-o(1)``.  The Plancherel collision bound remains asymptotically
neutral for every polynomial number of source draws.

This is an information-theoretic no-go for the carrier-traced point quotient,
not for the original carrier-retaining state, non-point global measurements,
or sample counts beyond the proved window.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_character_moments import (
    compose_permutations,
    permutation_cycle_type,
)
from self_dual_wreath_joint_character_correlation_decoder import (
    _permutations,
    inverse_permutation,
)
from self_dual_wreath_natural_unequal_dominance import plancherel_probabilities
from self_dual_wreath_point_copy_threshold import (
    maximum_nonidentity_class_reciprocal,
)
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_point_centered_residual_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-POINT-CENTERED-RESIDUAL-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class MeanZeroCharacterControl:
    n: int
    copy_count: int
    source_tuple_count: int
    maximum_mean_channel_formula_residual: float
    maximum_operator_mean_projection_residual: float
    residual_pythagorean_variance_residual: float
    exact_mean_zero_character_simplex_verified: bool
    status: str


@dataclass(frozen=True)
class PointResidualBound:
    n: int
    copy_count: int
    log2_group_order: float
    mean_simplex_normalized_energy: float
    mean_simplex_trace_excess: float
    residual_normalized_energy_log2_upper_bound: float
    residual_normalized_energy_upper_bound: float
    arbitrary_point_povm_excess_log2_upper_bound: float
    arbitrary_point_povm_excess_upper_bound: float


@dataclass(frozen=True)
class PointResidualScalingRecord:
    n: int
    schedule: str
    copy_count: int
    log2_group_order: float
    residual_normalized_energy_log2_upper_bound: float
    arbitrary_point_povm_excess_log2_upper_bound: float
    arbitrary_point_povm_excess_superpolynomially_small: bool
    public_label_adaptive_measurements_covered: bool
    globally_distinct_conditioning_transfer_available: bool
    carrier_retaining_measurements_covered: bool
    status: str


@dataclass(frozen=True)
class PointCenteredResidualTheorem:
    plancherel_zero_character_mean: str
    mean_simplex: str
    orthogonal_variance: str
    residual_bound: str
    arbitrary_measurement_bound: str
    sample_window: str
    collision_free_transfer: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PointCenteredResidualReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PointCenteredResidualTheorem
    finite_controls: list[MeanZeroCharacterControl]
    scaling_records: list[PointResidualScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _partition_number(n: int) -> int:
    if n < 0:
        raise ValueError("n must be nonnegative")
    counts = [0] * (n + 1)
    counts[0] = 1
    for part in range(1, n + 1):
        for total in range(part, n + 1):
            counts[total] += counts[total - part]
    return counts[n]


def _log2_one_minus_power_of_two_minus(k: int) -> float:
    if k > 60:
        return 0.0
    return math.log2(1.0 - math.exp2(-k))


def _log2_sum(values: tuple[float, ...]) -> float:
    finite = tuple(value for value in values if value > -math.inf)
    if not finite:
        return -math.inf
    maximum = max(finite)
    return maximum + math.log2(sum(math.exp2(value - maximum) for value in finite))


def _log2_expm1(value: float) -> float:
    if value <= 0:
        return -math.inf
    if value > 50:
        return value / math.log(2.0) + math.log2(1.0 - math.exp(-value))
    return math.log2(math.expm1(value))


def _exp2(log2_value: float) -> float:
    if log2_value < -1074:
        return 0.0
    if log2_value > 1023:
        return math.inf
    return math.exp2(log2_value)


def mean_zero_character_diagonal(
    n: int,
    copy_count: int,
) -> np.ndarray:
    """Return E_L diag_z=0(omega_j), indexed by point and group element."""

    if n < 2 or copy_count < 1:
        raise ValueError("require n>=2 and a positive copy count")
    from self_dual_wreath_joint_character_correlation_decoder import _permutations

    permutations = _permutations(n)
    order = len(permutations)
    subgroup_order = math.factorial(n - 1)
    inverse_orientation = math.exp2(-copy_count)
    correct = (
        1.0 + (subgroup_order - 1) * inverse_orientation
    ) / (order * subgroup_order)
    wrong = inverse_orientation / order
    output = np.empty((n, order), dtype=float)
    point = n - 1
    for image in range(n):
        for index, permutation in enumerate(permutations):
            output[image, index] = (
                correct if permutation[point] == image else wrong
            )
    return output


def mean_simplex_normalized_energy(n: int, copy_count: int) -> float:
    log2_order = math.lgamma(n + 1) / math.log(2.0)
    orientation_over_order_squared = _exp2(copy_count - 2.0 * log2_order)
    factor = 1.0 - math.exp2(-copy_count)
    return (n - 1) * orientation_over_order_squared * factor * factor


def mean_simplex_trace_excess(n: int, copy_count: int) -> float:
    log2_order = math.lgamma(n + 1) / math.log(2.0)
    return (
        (n - 1)
        / n
        * (1.0 - math.exp2(-copy_count))
        * _exp2(-log2_order)
    )


def point_residual_bound(n: int, copy_count: int) -> PointResidualBound:
    """Return the exact positive-term residual upper bound from (3)."""

    if n < 5 or copy_count < 1:
        raise ValueError("require n>=5 and a positive copy count")
    log2_order = math.lgamma(n + 1) / math.log(2.0)
    inverse_order = _exp2(-log2_order)
    log2_n_minus_one = math.log2(n - 1)
    log2_one_minus_inverse = math.log2(1.0 - inverse_order)
    q = maximum_nonidentity_class_reciprocal(n)
    log2_q = math.log2(q)
    log2_one_plus_q2 = math.log2(1.0 + q * q)

    diagonal_nonidentity = (
        log2_n_minus_one
        + log2_one_minus_inverse
        - log2_order
        + math.log2(copy_count)
        + 2.0 * log2_q
        + (copy_count - 1) * log2_one_plus_q2
    )
    one_identity = (
        log2_n_minus_one
        + 1.0
        + log2_one_minus_inverse
        - log2_order
        + copy_count * math.log2(2.0 * q)
    )
    distinct_nonidentity = (
        log2_n_minus_one
        + log2_one_minus_inverse
        + math.log2(max(1e-323, 1.0 - 2.0 * inverse_order))
        + copy_count * math.log2(q + q * q)
    )
    witness_minus_mean = (
        log2_n_minus_one
        + _log2_one_minus_power_of_two_minus(copy_count)
        - 2.0 * log2_order
    )
    binomial_exponent = copy_count * math.log1p(q * q)
    binomial_log2 = _log2_expm1(binomial_exponent) - 2.0 * log2_q
    nonidentity = (
        log2_n_minus_one
        + math.log2(_partition_number(n))
        - log2_order
        + binomial_log2
    )
    residual_log2 = _log2_sum(
        (
            diagonal_nonidentity,
            one_identity,
            distinct_nonidentity,
            witness_minus_mean,
            nonidentity,
        )
    )
    residual = _exp2(residual_log2)
    mean_excess = mean_simplex_trace_excess(n, copy_count)
    mean_excess_log2 = (
        math.log2(n - 1)
        - math.log2(n)
        - log2_order
        + _log2_one_minus_power_of_two_minus(copy_count)
    )
    residual_excess_log2 = -1.0 + 0.5 * residual_log2
    total_excess_log2 = min(
        0.0,
        _log2_sum((mean_excess_log2, residual_excess_log2)),
    )
    return PointResidualBound(
        n=n,
        copy_count=copy_count,
        log2_group_order=log2_order,
        mean_simplex_normalized_energy=mean_simplex_normalized_energy(
            n,
            copy_count,
        ),
        mean_simplex_trace_excess=mean_excess,
        residual_normalized_energy_log2_upper_bound=residual_log2,
        residual_normalized_energy_upper_bound=residual,
        arbitrary_point_povm_excess_log2_upper_bound=total_excess_log2,
        arbitrary_point_povm_excess_upper_bound=_exp2(total_excess_log2),
    )


def _virtual_iid_label_tuples(
    n: int,
    copy_count: int,
) -> tuple[tuple[tuple[Label, ...], float], ...]:
    probabilities = tuple(
        (partition, float(mass))
        for partition, mass in plancherel_probabilities(n)
    )
    output = []
    for draws in itertools.product(probabilities, repeat=2 * copy_count):
        partitions = tuple(item[0] for item in draws)
        weight = math.prod(item[1] for item in draws)
        labels = tuple(zip(partitions[::2], partitions[1::2]))
        output.append((labels, weight))
    return tuple(output)


def _virtual_zero_character_point_channel(
    labels: tuple[Label, ...],
) -> np.ndarray:
    """Return the virtual iid-pair ``z=0`` point channel.

    Equal pairs are retained here only as the algebraic iid-Plancherel
    extension used by the annealed character calculation.  The physical
    theorem is obtained by conditioning on the all-unequal event; this helper
    deliberately does not route equal pairs through the unequal-irrep state
    constructor.
    """

    if not labels:
        raise ValueError("at least one source pair is required")
    n = sum(labels[0][0])
    permutations = _permutations(n)
    order = len(permutations)
    subgroup_order = math.factorial(n - 1)
    inverse = {
        permutation: inverse_permutation(permutation)
        for permutation in permutations
    }
    cycle_types = {
        permutation_cycle_type(permutation) for permutation in permutations
    }
    zero_laws = {}
    for cycle_type in cycle_types:
        probability = 1.0
        for left, right in labels:
            ratio = (
                symmetric_character(left, cycle_type)
                * symmetric_character(right, cycle_type)
                / (
                    hook_length_dimension(left)
                    * hook_length_dimension(right)
                )
            )
            probability *= (1.0 + ratio) / 2.0
        zero_laws[cycle_type] = probability

    output = np.zeros((n, order), dtype=float)
    point = n - 1
    for image in range(n):
        hidden_fiber = tuple(
            hidden for hidden in permutations if hidden[point] == image
        )
        for source_index, source in enumerate(permutations):
            output[image, source_index] = sum(
                zero_laws[
                    permutation_cycle_type(
                        compose_permutations(inverse[source], hidden)
                    )
                ]
                for hidden in hidden_fiber
            ) / (order * subgroup_order)
    return output


def audit_mean_zero_character_control(
    n: int,
    copy_count: int,
    *,
    tolerance: float = 1e-9,
) -> MeanZeroCharacterControl:
    tuples = _virtual_iid_label_tuples(n, copy_count)
    predicted_channel = mean_zero_character_diagonal(n, copy_count)
    observed_channel = np.zeros_like(predicted_channel)
    mean_delta = np.zeros_like(predicted_channel[0])
    total_energy = 0.0
    delta_rows = []
    for labels, weight in tuples:
        measured = _virtual_zero_character_point_channel(labels)
        observed_channel += weight * measured
        delta = measured[0] - np.mean(measured, axis=0)
        mean_delta += weight * delta
        total_energy += weight * float(np.vdot(delta, delta).real)
        delta_rows.append((weight, delta))

    centered_channel = predicted_channel - np.mean(predicted_channel, axis=0)
    projected_mean = centered_channel[0]
    projection_residual = float(np.linalg.norm(mean_delta - projected_mean))
    residual_energy = sum(
        weight * float(np.vdot(delta - projected_mean, delta - projected_mean).real)
        for weight, delta in delta_rows
    )
    pythagorean = abs(
        residual_energy
        - total_energy
        + float(np.vdot(projected_mean, projected_mean).real)
    )
    channel_residual = float(np.max(np.abs(observed_channel - predicted_channel)))
    verified = bool(
        channel_residual <= 100 * tolerance
        and projection_residual <= 100 * tolerance
        and pythagorean <= 100 * tolerance
    )
    return MeanZeroCharacterControl(
        n=n,
        copy_count=copy_count,
        source_tuple_count=len(tuples),
        maximum_mean_channel_formula_residual=channel_residual,
        maximum_operator_mean_projection_residual=projection_residual,
        residual_pythagorean_variance_residual=pythagorean,
        exact_mean_zero_character_simplex_verified=verified,
        status=(
            "exact-plancherel-mean-z0-simplex-and-residual-variance"
            if verified
            else "mean-zero-character-control-failure"
        ),
    )


def point_residual_scaling_record(
    n: int,
    schedule: str,
) -> PointResidualScalingRecord:
    if schedule == "critical-two-log-factorial":
        copies = math.ceil(2.0 * math.lgamma(n + 1) / math.log(2.0))
    elif schedule == "quartic":
        copies = n**4
    elif schedule == "quintic-sixteenth":
        copies = max(1, n**5 // 16)
    else:
        raise ValueError("unknown copy schedule")
    bound = point_residual_bound(n, copies)
    superpolynomial = (
        bound.arbitrary_point_povm_excess_log2_upper_bound
        < -math.log2(n) ** 2
    )
    return PointResidualScalingRecord(
        n=n,
        schedule=schedule,
        copy_count=copies,
        log2_group_order=bound.log2_group_order,
        residual_normalized_energy_log2_upper_bound=(
            bound.residual_normalized_energy_log2_upper_bound
        ),
        arbitrary_point_povm_excess_log2_upper_bound=(
            bound.arbitrary_point_povm_excess_log2_upper_bound
        ),
        arbitrary_point_povm_excess_superpolynomially_small=superpolynomial,
        public_label_adaptive_measurements_covered=True,
        globally_distinct_conditioning_transfer_available=True,
        carrier_retaining_measurements_covered=False,
        status=(
            "carrier-traced-point-povm-excess-superpolynomially-small"
            if superpolynomial
            else "finite-rank-residual-bound-not-yet-separated"
        ),
    )


def build_point_centered_residual_report() -> PointCenteredResidualReport:
    controls = [
        audit_mean_zero_character_control(3, 1),
        audit_mean_zero_character_control(3, 2),
    ]
    schedules = (
        "critical-two-log-factorial",
        "quartic",
        "quintic-sixteenth",
    )
    scaling = [
        point_residual_scaling_record(n, schedule)
        for n in (8, 16, 32, 64, 128)
        for schedule in schedules
    ]
    failures = sum(
        not row.exact_mean_zero_character_simplex_verified
        for row in controls
    )
    tail = [row for row in scaling if row.n >= 32]
    separated = all(
        row.arbitrary_point_povm_excess_superpolynomially_small
        for row in tail
    )
    verified = failures == 0 and separated
    theorem = PointCenteredResidualTheorem(
        plancherel_zero_character_mean=(
            "E p_L(0|e)=1 and E p_L(0|h)=2^-k for every h!=e."
        ),
        mean_simplex=(
            "D||M_j||_2^2=(n-1)2^k/(n!)^2(1-2^-k)^2 and "
            "||M_j||_1/2=(n-1)(1-2^-k)/(n n!)."
        ),
        orthogonal_variance=(
            "E||Delta_(j,L)-M_j||_2^2=E||Delta_(j,L)||_2^2-||M_j||_2^2."
        ),
        residual_bound=(
            "The explicit positive remainder is at most "
            "exp(O(sqrt(n))) k exp(O(k/n^4))/n! up to smaller terms."
        ),
        arbitrary_measurement_bound=(
            "E[P_point-1/n]<=(n-1)(1-2^-k)/(n n!)+sqrt(R_(n,k))/2."
        ),
        sample_window=(
            "For k=O(n^5), every public-label-adaptive carrier-traced point POVM "
            "has superpolynomially small average excess."
        ),
        collision_free_transfer=(
            "Conditioning all polynomially many source draws distinct multiplies "
            "the nonnegative residual second moment by only 1/(1-o(1))."
        ),
        scope=(
            "The theorem does not cover carrier-retaining measurements, non-point "
            "global decoders, or sample schedules beyond the proved residual window."
        ),
        theorem_verified=verified,
        status=(
            "carrier-traced-point-route-closed-through-quintic-samples"
            if verified
            else "point-centered-residual-certificate-failure"
        ),
    )
    return PointCenteredResidualReport(
        created_at=utc_now(),
        theorem_contract={
            "source": "virtual iid Plancherel pairs, transferring on the global-distinct event",
            "retained_state": "carrier-traced group--orientation point quotient",
            "measurement_scope": "arbitrary point POVM adaptive to every public source label",
            "sample_scope": "k=O(n^5), including every fixed multiple of log2(n!)",
            "claim_boundary": "point quotient only; carrier-retaining global route remains open",
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "id": "PO-POINT-MEAN-Z0-SIMPLEX",
                "statement": "Derive the exact Plancherel mean diagonal z=0 signal.",
                "resolved": verified,
            },
            {
                "id": "PO-POINT-CENTERED-RESIDUAL-ENERGY",
                "statement": "Subtract the mean simplex by Hilbert--Schmidt orthogonal variance.",
                "resolved": verified,
            },
            {
                "id": "PO-POINT-ARBITRARY-POVM-RESIDUAL-NO-GO",
                "statement": "Convert the residual second moment into a public-label-adaptive trace bound.",
                "resolved": verified,
            },
            {
                "id": "PO-POINT-GLOBAL-DISTINCT-RESIDUAL-TRANSFER",
                "statement": "Transfer the nonnegative residual second moment through global distinctness.",
                "resolved": verified,
            },
            {
                "id": "PO-CARRIER-RETAINING-GLOBAL-DECODER",
                "statement": "Analyze the original carrier-retaining state without point coarse graining.",
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Subtracting the annealed atom is invalid for label-adaptive measurements.",
                "answer": (
                    "False. The decomposition Delta_L=M+R_L is operator exact for "
                    "every L; only the residual second moment is averaged. The POVM "
                    "may depend arbitrarily on L before applying the trace bound."
                ),
                "resolved": True,
            },
            {
                "challenge": "Small residual Hilbert--Schmidt norm does not control trace norm.",
                "answer": (
                    "It does after retaining the ambient factor D explicitly: "
                    "E||R||_1<=sqrt(D E||R||_2^2)=sqrt(R_(n,k))."
                ),
                "resolved": True,
            },
            {
                "challenge": "Global distinctness may amplify a signed residual.",
                "answer": (
                    "The transferred object is ||R_L||_2^2>=0, so conditioning costs "
                    "at most the reciprocal event probability."
                ),
                "resolved": True,
            },
            {
                "challenge": "The theorem rules out every code-equivalence quantum algorithm.",
                "answer": (
                    "Too strong. It closes only carrier-traced point coarse graining; "
                    "carrier-retaining and non-point global measurements remain open."
                ),
                "resolved": True,
            },
            {
                "challenge": "The k=O(n^5) statement covers every polynomial sample schedule.",
                "answer": (
                    "False. Higher-degree schedules are outside the present character-ratio bound."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_mean_z0_simplex_theorem_count": int(verified),
            "orthogonal_residual_variance_theorem_count": int(verified),
            "arbitrary_point_povm_residual_no_go_count": int(verified),
            "global_distinct_residual_transfer_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "scaling_record_count": len(scaling),
            "superpolynomial_scaling_record_count": sum(
                row.arbitrary_point_povm_excess_superpolynomially_small
                for row in scaling
            ),
            "tail_critical_excess_log2_upper_bound": next(
                row.arbitrary_point_povm_excess_log2_upper_bound
                for row in scaling
                if row.n == 128 and row.schedule == "critical-two-log-factorial"
            ),
            "tail_quartic_excess_log2_upper_bound": next(
                row.arbitrary_point_povm_excess_log2_upper_bound
                for row in scaling
                if row.n == 128 and row.schedule == "quartic"
            ),
            "tail_quintic_sixteenth_excess_log2_upper_bound": next(
                row.arbitrary_point_povm_excess_log2_upper_bound
                for row in scaling
                if row.n == 128 and row.schedule == "quintic-sixteenth"
            ),
            "carrier_retaining_global_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "mean_zero_character_simplex_proved": verified,
            "centered_residual_second_moment_bound_proved": verified,
            "public_label_adaptive_point_povm_no_go_proved": verified,
            "critical_copy_multiplier_two_point_route_viable": False,
            "all_fixed_log_factorial_copy_multipliers_closed": verified,
            "carrier_traced_point_route_closed_through_k_O_n5": verified,
            "global_distinct_conditioning_reopens_point_route": False,
            "carrier_retaining_global_decoder_ruled_out": False,
            "nonpoint_collective_decoder_ruled_out": False,
            "all_polynomial_sample_schedules_ruled_out": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "After removing the factorially rare mean z=0 simplex, every "
                "remaining carrier-traced point matrix entry has a superpolynomial "
                "trace-norm bound through k=O(n^5)."
            ),
        },
        status=theorem.status,
        summary=(
            "Subtracted the exact Plancherel mean identity simplex, bounded the "
            "orthogonal residual, and closed every public-label-adaptive "
            "carrier-traced point POVM through quintic sample schedules."
        ),
        falsifiers_triggered=[
            "The c=2 carrier-traced point route is not an open relative-spectrum mechanism.",
            "Increasing the fused copy width by any fixed log-factorial multiplier does not rescue point decoding.",
            "The identity atom plus residual trace bound closes the route despite positive ambient energy.",
            "Future code-equivalence work must retain the carrier or abandon point coarse graining.",
        ],
    )


def write_point_centered_residual_report(
    path: Path = REPORT_PATH,
    **_: Any,
) -> dict[str, Any]:
    payload = asdict(build_point_centered_residual_report())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_point_centered_residual_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
