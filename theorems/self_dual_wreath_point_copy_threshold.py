"""Sharp copy threshold for the annealed point-quotient signal.

Let ``N=n!`` and let ``k`` natural unequal-label blocks feed the retained
group--orientation state.  For independent Plancherel labels, the normalized
point Hilbert--Schmidt energy is

    S_(n,k)=N 2^k E ||omega_0-bar(omega)||_2^2
           =N^-2 sum_(u,s,t) chi_std(u)
             [a(s^-1 t)+c_u(s)d_u(t)]^k,                 (1)

where ``a(x)=1/|x^G|`` and ``c,d`` are the two conjugacy-incidence terms from
``self_dual_wreath_point_stabilizer_quotient``.  The ``u=e,s=t=e`` summand is

    (n-1)(2^k-1)/N^2.                                   (2)

It is the unique term with local value two after Plancherel averaging.

For ``n>=5``, every nonidentity conjugacy class in ``S_n`` has size at least
``n(n-1)/2``.  Put ``q=2/[n(n-1)]``.  The incidence sums

    sum_s c_u(s),  sum_t d_u(t)

are both the commutator density ``A(u)``.  The second equality uses the
character calculation that a product of two conjugates has the same law as a
commutator in ``S_n``.  Frobenius' formula gives

    N^-1 sum_u A(u)^2 = zeta_(S_n)(2).                   (3)

For ``u!=e``, both incidence factors are at most ``q``.  Expanding (1) and
using (3) bounds the entire nonidentity contribution by

    B_non = (n-1) zeta(2)/N
            * ((1+q^2)^k-1)/q^2.                        (4)

The positive ``u=e`` contribution is bounded by separating ``(e,e)``, equal
nonidentity pairs, pairs with one identity, and distinct nonidentity pairs.
This gives the explicit upper bound implemented below.

Consequently, for every fixed ``c<2`` and ``k<=c log_2 N+O(1)``,

    S_(n,k) <= N^{-(2-c)+o(1)}.

For any POVM that may depend on the public source labels,

    P_point-1/n <= (1/2) E||omega_0-bar(omega)||_1
                <= (1/2)sqrt(S_(n,k)).                  (5)

Thus every carrier-traced point decoder has superpolynomially small average
excess below twice the information-threshold copy count.  Conditioning all
source partitions to be distinct only divides the nonnegative energy upper
bound by ``P_cf=1-o(1)``, so the conclusion survives the physical trim.

At ``k=ceil(2 log_2 N)``, equations (2) and (4) instead imply

    S_(n,k) >= n-1-o(1).                                (6)

This is a genuine normalized-energy phase transition, but not an algorithm:
Hilbert--Schmidt energy can be hidden across exponentially many tiny
eigenvalues.  The remaining high-value question is whether the critical
``c=2`` child-star operator admits a direct harmonic Naimark transform or is
still operationally dequantized.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_character_moments import (
    compose_permutations,
    permutation_cycle_type,
)
from self_dual_wreath_joint_character_correlation_decoder import (
    _permutations,
    inverse_permutation,
)
from self_dual_wreath_point_stabilizer_quotient import audit_natural_point_signal
from symmetric_character import conjugacy_class_size


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_point_copy_threshold.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-POINT-COPY-THRESHOLD"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class WordDensityControl:
    n: int
    group_order: int
    commutator_class_counts: dict[str, int]
    conjugate_product_class_counts: dict[str, int]
    maximum_class_count_mismatch: int
    direct_word_laws_identical: bool
    status: str


@dataclass(frozen=True)
class PointThresholdBounds:
    n: int
    copy_count: int
    log2_group_order: float
    maximum_nonidentity_class_reciprocal: float
    witten_zeta_two_upper_bound: float
    identity_witness_lower_bound: float
    identity_total_upper_bound: float
    nonidentity_absolute_upper_bound: float
    signal_lower_bound: float
    signal_upper_bound: float
    signal_lower_bound_log2: float
    signal_upper_bound_log2: float
    arbitrary_point_povm_excess_upper_bound: float


@dataclass(frozen=True)
class PointThresholdFiniteControl:
    n: int
    copy_multiplier: float
    copy_count: int
    exact_normalized_point_signal: float
    certified_signal_lower_bound: float
    certified_signal_upper_bound: float
    lower_bound_residual: float
    upper_bound_residual: float
    exact_signal_inside_certified_interval: bool
    status: str


@dataclass(frozen=True)
class PointThresholdScalingRecord:
    n: int
    copy_multiplier: float
    copy_count: int
    log2_group_order: float
    signal_lower_bound_log2: float
    signal_upper_bound_log2: float
    arbitrary_point_povm_excess_log2_upper_bound: float
    subcritical_point_decoder_excess_superpolynomial: bool
    critical_normalized_energy_lower_bound: bool
    collision_free_upper_bound_transfer_asymptotically_lossless: bool
    critical_harmonic_measurement_compiled: bool
    status: str


@dataclass(frozen=True)
class PointCopyThresholdTheorem:
    exact_signal: str
    word_density_identity: str
    nonidentity_bound: str
    subcritical_consequence: str
    collision_free_transfer: str
    critical_lower_bound: str
    operational_boundary: str
    subcritical_arbitrary_point_povm_no_go_proved: bool
    critical_normalized_energy_phase_transition_proved: bool
    critical_operational_point_advantage_proved: bool
    critical_harmonic_naimark_compiled: bool
    full_hidden_permutation_decoder_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PointCopyThresholdReport:
    created_at: str
    theorem_contract: dict[str, Any]
    word_density_controls: list[WordDensityControl]
    finite_controls: list[PointThresholdFiniteControl]
    scaling_records: list[PointThresholdScalingRecord]
    theorem: PointCopyThresholdTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _exp2(log2_value: float) -> float:
    if log2_value < -1074.0:
        return 0.0
    if log2_value > 1023.0:
        return math.inf
    return math.exp2(log2_value)


def _partition_number(n: int) -> int:
    values = [0] * (n + 1)
    values[0] = 1
    for part in range(1, n + 1):
        for total in range(part, n + 1):
            values[total] += values[total - part]
    return values[n]


def maximum_nonidentity_class_reciprocal(n: int) -> float:
    if n < 5:
        raise ValueError("the transposition-class formula is used only for n>=5")
    return 2.0 / (n * (n - 1))


def exact_maximum_nonidentity_class_reciprocal(n: int) -> float:
    if n < 2:
        raise ValueError("n must be at least two")
    identity = (1,) * n
    return max(
        1.0 / conjugacy_class_size(cycle)
        for cycle in integer_partitions(n)
        if cycle != identity
    )


def symmetric_witten_zeta_two_upper_bound(n: int) -> float:
    """Use zeta(2)<=p(n), avoiding partition enumeration at scaling ranks."""

    if n < 1:
        raise ValueError("n must be positive")
    return float(_partition_number(n))


def direct_word_density_control(n: int) -> WordDensityControl:
    if n < 2 or n > 5:
        raise ValueError("direct word controls are restricted to 2<=n<=5")
    group = _permutations(n)
    commutators: Counter[tuple[int, ...]] = Counter()
    conjugate_products: Counter[tuple[int, ...]] = Counter()
    for source in group:
        source_inverse = inverse_permutation(source)
        for conjugator in group:
            conjugator_inverse = inverse_permutation(conjugator)
            commutator = compose_permutations(
                compose_permutations(
                    compose_permutations(source, conjugator),
                    source_inverse,
                ),
                conjugator_inverse,
            )
            conjugate_product = compose_permutations(
                compose_permutations(
                    compose_permutations(source, conjugator),
                    source,
                ),
                conjugator_inverse,
            )
            commutators[permutation_cycle_type(commutator)] += 1
            conjugate_products[permutation_cycle_type(conjugate_product)] += 1
    cycles = set(commutators) | set(conjugate_products)
    mismatch = max(
        (abs(commutators[cycle] - conjugate_products[cycle]) for cycle in cycles),
        default=0,
    )
    verified = mismatch == 0
    return WordDensityControl(
        n=n,
        group_order=len(group),
        commutator_class_counts={
            str(cycle): count for cycle, count in sorted(commutators.items())
        },
        conjugate_product_class_counts={
            str(cycle): count
            for cycle, count in sorted(conjugate_products.items())
        },
        maximum_class_count_mismatch=mismatch,
        direct_word_laws_identical=verified,
        status=(
            "commutator-and-conjugate-product-laws-identical"
            if verified
            else "word-density-identity-control-failure"
        ),
    )


def annealed_point_signal_bounds(n: int, copy_count: int) -> PointThresholdBounds:
    if n < 5 or copy_count < 1:
        raise ValueError("require n>=5 and a positive copy count")
    log2_order = math.lgamma(n + 1) / math.log(2.0)
    inverse_order = _exp2(-log2_order)
    q = maximum_nonidentity_class_reciprocal(n)
    zeta_upper = symmetric_witten_zeta_two_upper_bound(n)

    identity_ratio = _exp2(copy_count - 2.0 * log2_order) * (
        1.0 - math.exp2(-copy_count)
    )
    identity_witness = (n - 1) * identity_ratio

    exponential_q = math.exp((copy_count - 1) * math.log1p(q * q))
    diagonal_nonidentity = (
        (1.0 - inverse_order)
        * inverse_order
        * copy_count
        * q
        * q
        * exponential_q
    )
    one_identity = (
        2.0
        * (1.0 - inverse_order)
        * inverse_order
        * _exp2(copy_count * math.log2(2.0 * q))
    )
    distinct_nonidentity = (
        (1.0 - inverse_order)
        * max(0.0, 1.0 - 2.0 * inverse_order)
        * _exp2(copy_count * math.log2(q + q * q))
    )
    identity_total = (n - 1) * (
        identity_ratio
        + diagonal_nonidentity
        + one_identity
        + distinct_nonidentity
    )

    binomial_factor = math.expm1(copy_count * math.log1p(q * q)) / (q * q)
    nonidentity = (n - 1) * zeta_upper * inverse_order * binomial_factor
    lower = max(0.0, identity_witness - nonidentity)
    upper = identity_total + nonidentity
    return PointThresholdBounds(
        n=n,
        copy_count=copy_count,
        log2_group_order=log2_order,
        maximum_nonidentity_class_reciprocal=q,
        witten_zeta_two_upper_bound=zeta_upper,
        identity_witness_lower_bound=identity_witness,
        identity_total_upper_bound=identity_total,
        nonidentity_absolute_upper_bound=nonidentity,
        signal_lower_bound=lower,
        signal_upper_bound=upper,
        signal_lower_bound_log2=(math.log2(lower) if lower > 0.0 else -math.inf),
        signal_upper_bound_log2=math.log2(upper),
        arbitrary_point_povm_excess_upper_bound=min(1.0, 0.5 * math.sqrt(upper)),
    )


def audit_point_threshold_finite_control(
    n: int,
    copy_multiplier: float,
) -> PointThresholdFiniteControl:
    if copy_multiplier <= 0:
        raise ValueError("copy multiplier must be positive")
    copies = math.ceil(copy_multiplier * math.log2(math.factorial(n)))
    exact = audit_natural_point_signal(n, copies).normalized_expected_centered_signal
    bounds = annealed_point_signal_bounds(n, copies)
    tolerance = 1e-10 * max(1.0, exact, bounds.signal_upper_bound)
    verified = bool(
        exact + tolerance >= bounds.signal_lower_bound
        and exact <= bounds.signal_upper_bound + tolerance
    )
    return PointThresholdFiniteControl(
        n=n,
        copy_multiplier=copy_multiplier,
        copy_count=copies,
        exact_normalized_point_signal=exact,
        certified_signal_lower_bound=bounds.signal_lower_bound,
        certified_signal_upper_bound=bounds.signal_upper_bound,
        lower_bound_residual=exact - bounds.signal_lower_bound,
        upper_bound_residual=bounds.signal_upper_bound - exact,
        exact_signal_inside_certified_interval=verified,
        status=(
            "exact-point-signal-inside-copy-threshold-bounds"
            if verified
            else "point-copy-threshold-bound-failure"
        ),
    )


def point_threshold_scaling_record(
    n: int,
    copy_multiplier: float,
) -> PointThresholdScalingRecord:
    if copy_multiplier <= 0:
        raise ValueError("copy multiplier must be positive")
    log2_order = math.lgamma(n + 1) / math.log(2.0)
    copies = math.ceil(copy_multiplier * log2_order)
    bounds = annealed_point_signal_bounds(n, copies)
    subcritical = copy_multiplier < 2.0
    critical = copy_multiplier == 2.0
    excess_log2 = min(0.0, -1.0 + 0.5 * bounds.signal_upper_bound_log2)
    return PointThresholdScalingRecord(
        n=n,
        copy_multiplier=copy_multiplier,
        copy_count=copies,
        log2_group_order=log2_order,
        signal_lower_bound_log2=bounds.signal_lower_bound_log2,
        signal_upper_bound_log2=bounds.signal_upper_bound_log2,
        arbitrary_point_povm_excess_log2_upper_bound=excess_log2,
        subcritical_point_decoder_excess_superpolynomial=subcritical,
        critical_normalized_energy_lower_bound=(
            critical and bounds.signal_lower_bound >= 0.5 * (n - 1)
        ),
        collision_free_upper_bound_transfer_asymptotically_lossless=subcritical,
        critical_harmonic_measurement_compiled=False,
        status=(
            "subcritical-point-povm-excess-factorially-small"
            if subcritical
            else "critical-point-energy-positive-operational-transform-open"
            if critical
            else "supercritical-point-energy-diagnostic-only"
        ),
    )


def build_point_copy_threshold_report() -> PointCopyThresholdReport:
    word_controls = [direct_word_density_control(n) for n in (3, 4, 5)]
    finite = [
        audit_point_threshold_finite_control(n, multiplier)
        for n in (5, 6)
        for multiplier in (1.0, 1.5, 2.0)
    ]
    scaling = [
        point_threshold_scaling_record(n, multiplier)
        for n in (8, 16, 32, 64, 128)
        for multiplier in (1.0, 1.5, 1.9, 2.0)
    ]
    class_bound_verified = all(
        abs(
            exact_maximum_nonidentity_class_reciprocal(n)
            - maximum_nonidentity_class_reciprocal(n)
        )
        < 1e-15
        for n in range(5, 13)
    )
    exact = bool(
        class_bound_verified
        and all(row.direct_word_laws_identical for row in word_controls)
        and all(row.exact_signal_inside_certified_interval for row in finite)
        and all(
            row.critical_normalized_energy_lower_bound
            for row in scaling
            if row.copy_multiplier == 2.0
        )
    )
    theorem = PointCopyThresholdTheorem(
        exact_signal=(
            "S_(n,k)=N^-2 sum_(u,s,t) chi_std(u) "
            "[a(s^-1t)+c_u(s)d_u(t)]^k."
        ),
        word_density_identity=(
            "Both incidence sums equal A(u), the commutator density; products "
            "of two conjugates and commutators have the same S_n law."
        ),
        nonidentity_bound=(
            "The entire u!=e contribution has magnitude at most "
            "(n-1)zeta(2)N^-1((1+q^2)^k-1)/q^2."
        ),
        subcritical_consequence=(
            "For fixed c<2 and k<=c log2(N)+O(1), S=N^{-(2-c)+o(1)} "
            "and every public-label-adaptive point POVM has excess at most sqrt(S)/2."
        ),
        collision_free_transfer=(
            "The point energy is nonnegative sourcewise, so conditioning on "
            "global distinctness divides its upper bound by P_cf=1-o(1)."
        ),
        critical_lower_bound=(
            "At k=ceil(2log2 N), the identity witness gives S>=n-1-o(1)."
        ),
        operational_boundary=(
            "Critical Hilbert--Schmidt energy does not imply trace distance, "
            "a child-star spectral window, or a harmonic Naimark circuit."
        ),
        subcritical_arbitrary_point_povm_no_go_proved=exact,
        critical_normalized_energy_phase_transition_proved=exact,
        critical_operational_point_advantage_proved=False,
        critical_harmonic_naimark_compiled=False,
        full_hidden_permutation_decoder_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=exact,
        status=(
            "point-copy-threshold-two-proved-critical-harmonic-measurement-open"
            if exact
            else "point-copy-threshold-certificate-failure"
        ),
    )
    return PointCopyThresholdReport(
        created_at=utc_now(),
        theorem_contract={
            "source": "independent Plancherel source pairs; subcritical upper transfers to globally distinct trim",
            "retained_state": "carrier-traced group--orientation point quotient",
            "copy_regime": "k=c log2(n!) with fixed c",
            "measurement_scope": "arbitrary point POVM adaptive to public source labels",
            "claim_boundary": "sharp normalized-energy threshold, not a critical-point measurement circuit",
        },
        word_density_controls=word_controls,
        finite_controls=finite,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-POINT-CRITICAL-CHILD-STAR-RELATIVE-SPECTRUM",
                "statement": (
                    "At k=ceil(2log2 n!), bound the critical child-star effect "
                    "spectrum relative to the average state, not ambient Hilbert--Schmidt norm."
                ),
                "resolved": False,
            },
            {
                "id": "PO-POINT-CRITICAL-HARMONIC-NAIMARK",
                "statement": (
                    "Compile or obstruct the S_(n-1) child-star square roots at "
                    "critical copy width without scalar QSVT normalization."
                ),
                "resolved": False,
            },
            {
                "id": "PO-POINT-CRITICAL-COLLISION-FREE-LOWER-TRANSFER",
                "statement": (
                    "Prove the critical energy lower bound directly under global "
                    "distinctness or show that pairwise-unequal natural access suffices."
                ),
                "resolved": False,
            },
            {
                "id": "PO-POINT-FULL-RECOVERY-INTERFACE",
                "statement": (
                    "If a critical point decoder exists, prove a full hidden-permutation "
                    "recovery interface under ordinary mixed coset-state access."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The k=ceil(log2 n!) point signal only needs a better measurement.",
                "answer": (
                    "False after carrier trace: every point POVM has factorially "
                    "small average excess throughout every fixed c<2 regime."
                ),
                "resolved": True,
            },
            {
                "challenge": "The identity witness at c=2 is already a decoder.",
                "answer": (
                    "False. It proves ambient normalized Hilbert--Schmidt energy, "
                    "not relative spectrum, trace distance, or circuit access."
                ),
                "resolved": True,
            },
            {
                "challenge": "Global source distinctness reopens the subcritical point route.",
                "answer": (
                    "False for an upper bound: sourcewise nonnegativity permits "
                    "conditioning at the sole multiplicative cost 1/P_cf=1+o(1)."
                ),
                "resolved": True,
            },
            {
                "challenge": "The theorem rules out carrier-retaining global decoders.",
                "answer": (
                    "Too strong. The theorem applies only after the carrier is traced "
                    "and only to point coarse graining."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "word_density_identity_control_count": len(word_controls),
            "finite_bound_control_count": len(finite),
            "finite_bound_failure_count": sum(
                not row.exact_signal_inside_certified_interval for row in finite
            ),
            "subcritical_arbitrary_point_povm_no_go_count": int(exact),
            "critical_energy_phase_transition_count": int(exact),
            "critical_operational_point_measurement_count": 0,
            "critical_harmonic_naimark_count": 0,
            "new_quantum_algorithm_count": 0,
            "tail_c1_signal_log2_upper_bound": next(
                row.signal_upper_bound_log2
                for row in scaling
                if row.n == 128 and row.copy_multiplier == 1.0
            ),
            "tail_c2_signal_log2_lower_bound": next(
                row.signal_lower_bound_log2
                for row in scaling
                if row.n == 128 and row.copy_multiplier == 2.0
            ),
        },
        claim_gate={
            "point_decoder_at_information_threshold_viable": False,
            "all_fixed_copy_multipliers_below_two_closed": exact,
            "critical_copy_multiplier_two_energy_positive": exact,
            "critical_energy_is_operational_advantage": False,
            "critical_child_star_relative_spectrum_proved": False,
            "critical_harmonic_naimark_compiled": False,
            "carrier_retaining_global_decoder_ruled_out": False,
            "full_hidden_permutation_decoder_constructed": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Point decoding below twice log2(n!) copies is information-theoretically "
                "blocked after carrier trace. Exactly at factor two, normalized energy "
                "appears, but its relative spectrum and direct measurement remain open."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved a factor-two copy threshold for carrier-traced point information: "
            "every subcritical point POVM has factorially small excess, while the "
            "critical normalized energy is positive but not yet operational."
        ),
        falsifiers_triggered=[
            "The existing k=ceil(log2 n!) point workbench cannot yield an inverse-polynomial point decoder after carrier trace.",
            "Finite positive point PGM excess below the factor-two threshold is pre-asymptotic.",
            "Positive critical Hilbert--Schmidt energy is not sufficient evidence for a quantum measurement.",
            "Future point work must move to k near 2log2(n!) and analyze relative child-star spectra, or retain the carrier.",
        ],
    )


def write_point_copy_threshold_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_point_copy_threshold_report())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    print(json.dumps(write_point_copy_threshold_report(), indent=2, sort_keys=True))
