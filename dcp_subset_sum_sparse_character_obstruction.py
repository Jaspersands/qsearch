"""Adaptive sparse-character obstruction for density-one subset sum.

For labels ``a=(a_1,...,a_m)`` in ``Z_N``, ``N=2^n``, define

    P_a(r) = product_i (1 + exp(2 pi i r a_i / N)).

The exact number of Boolean witnesses for target ``t`` is

    F_a(t) = N^-1 sum_r P_a(r) exp(-2 pi i r t / N).

This module proves a source-uniform obstruction against approximating the
nonzero-frequency part with polynomially many characters, even if the
frequencies are chosen after all labels and the target are visible.

Let ``q`` be the additive order of ``r``.  If ``q<=T``, then ``P_a(r)=0``
whenever one label lands at the antipodal residue, which happens independently
with probability ``1/q`` per label.  A union bound controls every low-order
frequency.  If ``q>T`` and ``s=T``, then

    E |1 + zeta_q^A|^(2s) = binomial(2s,s)

because ``q>s`` prevents nonzero exponent aliases.  Markov and a union bound
over every nonzero frequency control the high-order terms simultaneously.

Taking ``T=floor(m/log_2(m)^2)`` proves that, for every fixed ``A``, with
superpolynomially high source probability,

    max_(r != 0) |P_a(r)| <= 2^m / m^A.

Therefore any adaptively selected set of at most ``m^B`` nonzero characters
contributes at most ``2^(m-n) m^(B-A)`` to every target.  The result closes
polynomially sparse character truncations, not dense implicit contractions,
non-Fourier algorithms, coherent sums over exponentially many frequencies, or
witness extraction from some other statistic.
"""

from __future__ import annotations

import cmath
import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_SPARSE_CHARACTER_PATH = Path(
    "research/classical_baselines/"
    "dcp_subset_sum_sparse_character_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-DHS-DCP-SUBSET-SUM-ADAPTIVE-SPARSE-CHARACTER-OBSTRUCTION"
)
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class SparseCharacterTheoremCertificate:
    exact_fourier_identity: str
    low_order_annihilation_bound: str
    high_order_moment_identity: str
    high_order_simultaneous_bound: str
    adaptive_sparse_selection_bound: str
    truncation_schedule: str
    source_failure_is_superpolynomial: bool
    full_label_adaptive_selection_covered: bool
    proof: str
    limitations: list[str]


@dataclass(frozen=True)
class ExactSparseCharacterControl:
    n_bits: int
    modulus: int
    register_count: int
    label_vector: list[int]
    target_count: int
    maximum_fourier_inversion_error: float
    fourier_identity_verified: bool
    moment_order: int
    checked_character_orders: list[int]
    maximum_root_moment_error: float
    root_moment_identity_verified: bool
    low_order_frequency_count: int
    low_order_annihilated_count: int


@dataclass(frozen=True)
class SparseCharacterScalingRow:
    n_bits: int
    register_count: int
    register_offset: int
    moment_order: int
    amplitude_gap_power: int
    selected_frequency_power: int
    residual_inverse_polynomial_degree: int
    log2_low_order_failure_upper_bound: float
    log2_high_order_failure_upper_bound: float
    log2_total_source_failure_upper_bound: float
    total_source_failure_upper_bound: float
    log2_selected_nonzero_contribution_upper_bound: float
    selected_nonzero_contribution_upper_bound: float
    finite_source_failure_bound_below_one: bool
    finite_selected_contribution_below_one: bool
    asymptotic_superpolynomial_source_success_proved: bool
    finite_row_is_computational_lower_bound: bool


@dataclass(frozen=True)
class DCPSubsetSumSparseCharacterReport:
    created_at: str
    theorem_contract: dict[str, str]
    theorem_certificate: SparseCharacterTheoremCertificate
    exact_controls: list[ExactSparseCharacterControl]
    rows: list[SparseCharacterScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def character_order(modulus: int, frequency: int) -> int:
    if modulus < 2 or modulus & (modulus - 1):
        raise ValueError("modulus must be a power of two")
    frequency %= modulus
    if frequency == 0:
        return 1
    return modulus // math.gcd(modulus, frequency)


def subset_sum_counts(
    labels: Sequence[int],
    modulus: int,
) -> list[int]:
    counts = [0] * modulus
    for assignment in itertools.product((0, 1), repeat=len(labels)):
        target = sum(
            int(label) * bit
            for label, bit in zip(labels, assignment)
        ) % modulus
        counts[target] += 1
    return counts


def character_products(
    labels: Sequence[int],
    modulus: int,
) -> list[complex]:
    root = cmath.exp(2j * math.pi / modulus)
    return [
        math.prod(1.0 + root ** (frequency * int(label)) for label in labels)
        for frequency in range(modulus)
    ]


def inverse_character_counts(
    products: Sequence[complex],
) -> list[complex]:
    modulus = len(products)
    root = cmath.exp(-2j * math.pi / modulus)
    return [
        sum(
            value * root ** (frequency * target)
            for frequency, value in enumerate(products)
        )
        / modulus
        for target in range(modulus)
    ]


def discrete_root_moment(character_order_value: int, moment_order: int) -> float:
    if character_order_value < 2 or moment_order < 1:
        raise ValueError("invalid order or moment")
    root = cmath.exp(2j * math.pi / character_order_value)
    return sum(
        abs(1.0 + root**residue) ** (2 * moment_order)
        for residue in range(character_order_value)
    ) / character_order_value


def exact_sparse_character_control(
    n_bits: int = 3,
    labels: Sequence[int] = (1, 3, 4, 6),
    moment_order: int = 2,
) -> ExactSparseCharacterControl:
    modulus = 1 << n_bits
    if any(not 0 <= int(label) < modulus for label in labels):
        raise ValueError("label outside modulus")
    counts = subset_sum_counts(labels, modulus)
    products = character_products(labels, modulus)
    reconstructed = inverse_character_counts(products)
    maximum_error = max(
        abs(value - expected)
        for value, expected in zip(reconstructed, counts)
    )
    checked_orders = [
        order
        for order in (4, 8, 16)
        if order > moment_order
    ]
    moment_errors = [
        abs(
            discrete_root_moment(order, moment_order)
            - math.comb(2 * moment_order, moment_order)
        )
        for order in checked_orders
    ]
    low_frequencies = [
        frequency
        for frequency in range(1, modulus)
        if character_order(modulus, frequency) <= moment_order
    ]
    annihilated = sum(
        abs(products[frequency]) <= 1e-10
        for frequency in low_frequencies
    )
    return ExactSparseCharacterControl(
        n_bits=n_bits,
        modulus=modulus,
        register_count=len(labels),
        label_vector=[int(label) for label in labels],
        target_count=modulus,
        maximum_fourier_inversion_error=maximum_error,
        fourier_identity_verified=maximum_error <= 1e-9,
        moment_order=moment_order,
        checked_character_orders=checked_orders,
        maximum_root_moment_error=max(moment_errors, default=0.0),
        root_moment_identity_verified=max(moment_errors, default=0.0) <= 1e-9,
        low_order_frequency_count=len(low_frequencies),
        low_order_annihilated_count=annihilated,
    )


def _log2_add(left: float, right: float) -> float:
    if left == -math.inf:
        return right
    if right == -math.inf:
        return left
    maximum = max(left, right)
    return maximum + math.log2(
        math.exp2(left - maximum) + math.exp2(right - maximum)
    )


def _low_order_failure_log2(
    register_count: int,
    moment_order: int,
) -> float:
    terms: list[float] = []
    order = 2
    while order <= moment_order:
        frequency_count = order // 2
        terms.append(
            math.log2(frequency_count)
            + register_count * math.log2(1.0 - 1.0 / order)
        )
        order <<= 1
    total = -math.inf
    for term in terms:
        total = _log2_add(total, term)
    return total


def _central_binomial_log2(moment_order: int) -> float:
    return (
        math.lgamma(2 * moment_order + 1)
        - 2 * math.lgamma(moment_order + 1)
    ) / math.log(2.0)


def sparse_character_scaling_row(
    n_bits: int,
    register_offset: int = 2,
    amplitude_gap_power: int = 12,
    selected_frequency_power: int = 4,
) -> SparseCharacterScalingRow:
    if n_bits < 8:
        raise ValueError("n_bits must be at least 8")
    if register_offset < 0:
        raise ValueError("register_offset must be nonnegative")
    if amplitude_gap_power < 1 or selected_frequency_power < 0:
        raise ValueError("invalid polynomial powers")
    register_count = n_bits + register_offset
    log_register_count = math.log2(register_count)
    moment_order = max(
        1,
        int(register_count // (log_register_count * log_register_count)),
    )
    low_log2 = _low_order_failure_log2(register_count, moment_order)
    threshold_log2 = (
        register_count
        - amplitude_gap_power * log_register_count
    )
    high_log2 = (
        n_bits
        + register_count * _central_binomial_log2(moment_order)
        - 2 * moment_order * threshold_log2
    )
    total_log2 = min(0.0, _log2_add(low_log2, high_log2))
    contribution_log2 = (
        register_offset
        + (selected_frequency_power - amplitude_gap_power)
        * log_register_count
    )
    return SparseCharacterScalingRow(
        n_bits=n_bits,
        register_count=register_count,
        register_offset=register_offset,
        moment_order=moment_order,
        amplitude_gap_power=amplitude_gap_power,
        selected_frequency_power=selected_frequency_power,
        residual_inverse_polynomial_degree=(
            amplitude_gap_power - selected_frequency_power
        ),
        log2_low_order_failure_upper_bound=low_log2,
        log2_high_order_failure_upper_bound=high_log2,
        log2_total_source_failure_upper_bound=total_log2,
        total_source_failure_upper_bound=math.exp2(total_log2),
        log2_selected_nonzero_contribution_upper_bound=contribution_log2,
        selected_nonzero_contribution_upper_bound=math.exp2(
            contribution_log2
        ),
        finite_source_failure_bound_below_one=(
            low_log2 < 0.0 and high_log2 < 0.0
        ),
        finite_selected_contribution_below_one=contribution_log2 < 0.0,
        asymptotic_superpolynomial_source_success_proved=True,
        finite_row_is_computational_lower_bound=False,
    )


def theorem_certificate() -> SparseCharacterTheoremCertificate:
    return SparseCharacterTheoremCertificate(
        exact_fourier_identity=(
            "F_a(t)=2^-n sum_r P_a(r) exp(-2 pi i r t/2^n)"
        ),
        low_order_annihilation_bound=(
            "Pr[exists nonzero r of order q<=T with P_a(r)!=0] "
            "<= sum_(q power of 2, q<=T) phi(q)(1-1/q)^m "
            "<= T exp(-m/T)"
        ),
        high_order_moment_identity=(
            "for character order q>s, "
            "E|1+zeta_q^A|^(2s)=binomial(2s,s)"
        ),
        high_order_simultaneous_bound=(
            "Pr[exists r of order >s with |P_a(r)|>2^m/m^A] "
            "<= 2^n binomial(2s,s)^m /(2^m/m^A)^(2s)"
        ),
        adaptive_sparse_selection_bound=(
            "on the simultaneous event, every label/target-adaptive set R "
            "with |R|<=m^B has |2^-n sum_(r in R) P_a(r)e(-rt/N)| "
            "<=2^(m-n)m^(B-A)"
        ),
        truncation_schedule="s=T=floor(m/log_2(m)^2)",
        source_failure_is_superpolynomial=True,
        full_label_adaptive_selection_covered=True,
        proof=(
            "Fourier inversion follows by expanding the Boolean generating "
            "product and applying character orthogonality. For low-order r, "
            "one antipodal label makes a factor zero; union over exact character "
            "orders. For q>s, expanding |1+zeta^A|^(2s) leaves only equal "
            "binomial exponents because their difference has magnitude at most "
            "s<q. Independence across labels, Markov, and a union over all "
            "frequencies give the high-order bound. The standard central-binomial "
            "bound gives high failure 2^n(s+1)^(-m/2)m^(2As), while low failure "
            "is at most s exp(-m/s). With s=m/log_2(m)^2, both are "
            "superpolynomially small. The event is simultaneous over every "
            "frequency, so post-label adaptive sparse selection is covered."
        ),
        limitations=[
            "The theorem assumes independent uniform labels in Z_(2^n) and m=n+O(1).",
            "The zero frequency is the target-independent baseline 2^(m-n).",
            "Dense implicit contractions over exponentially many frequencies are not covered.",
            "Coherent quantum interference across the full character set is not covered.",
            "Non-Fourier arithmetic, lattice, and reduced-basis algorithms are not covered.",
            "The result blocks a sparse truncation; it is not a general computational lower bound.",
            "A small count approximation would not by itself provide a Boolean witness decoder.",
        ],
    )


def run_sparse_character_obstruction(
    n_values: Sequence[int] = (512, 1024, 4096, 16384, 65536),
    register_offset: int = 2,
    amplitude_gap_power: int = 12,
    selected_frequency_power: int = 4,
) -> DCPSubsetSumSparseCharacterReport:
    if not n_values:
        raise ValueError("at least one scaling size is required")
    controls = [exact_sparse_character_control()]
    rows = [
        sparse_character_scaling_row(
            n_bits,
            register_offset=register_offset,
            amplitude_gap_power=amplitude_gap_power,
            selected_frequency_power=selected_frequency_power,
        )
        for n_bits in n_values
    ]
    control_failures = sum(
        (not control.fourier_identity_verified)
        + (not control.root_moment_identity_verified)
        for control in controls
    )
    tail_rows = [row for row in rows if row.n_bits == max(n_values)]
    metrics: dict[str, int | float] = {
        "exact_control_count": len(controls),
        "exact_fourier_target_count": sum(
            control.target_count for control in controls
        ),
        "exact_control_failure_count": control_failures,
        "exact_root_moment_identity_count": sum(
            control.root_moment_identity_verified for control in controls
        ),
        "low_order_annihilation_theorem_count": 1,
        "high_order_simultaneous_moment_theorem_count": 1,
        "adaptive_sparse_selection_theorem_count": 1,
        "scaling_row_count": len(rows),
        "finite_source_failure_bound_below_one_row_count": sum(
            row.finite_source_failure_bound_below_one for row in rows
        ),
        "maximum_n_bits": max(n_values),
        "tail_source_failure_probability_upper_bound": max(
            row.total_source_failure_upper_bound for row in tail_rows
        ),
        "tail_selected_nonzero_contribution_upper_bound": max(
            row.selected_nonzero_contribution_upper_bound
            for row in tail_rows
        ),
        "proved_full_label_adaptive_sparse_character_obstruction_count": 1,
        "proved_dense_implicit_character_obstruction_count": 0,
        "proved_general_computational_lower_bound_count": 0,
        "polynomial_witness_decoder_count": 0,
    }
    return DCPSubsetSumSparseCharacterReport(
        created_at=utc_now(),
        theorem_contract={
            "source": (
                "m=n+c independent uniform labels in Z_(2^n), with fixed c"
            ),
            "selector_access": (
                "the frequency set may depend arbitrarily on every public label "
                "and on the target"
            ),
            "selector_size": "at most m^B nonzero characters for fixed B",
            "observable": (
                "the corresponding truncated exact subset-sum Fourier inversion"
            ),
            "conclusion": (
                "uniform superpolynomial-probability amplitude obstruction for "
                "every fixed polynomial gap and every adaptive sparse selector"
            ),
        },
        theorem_certificate=theorem_certificate(),
        exact_controls=controls,
        rows=rows,
        headline_metrics=metrics,
        claim_gate={
            "exact_controls_pass": control_failures == 0,
            "full_label_adaptive_sparse_character_routes_closed": True,
            "dense_implicit_character_contractions_closed": False,
            "coherent_full_character_measurements_closed": False,
            "non_fourier_algorithms_closed": False,
            "polynomial_witness_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Even a selector that sees all labels cannot rescue only "
                "polynomially many subset-sum characters. Any surviving Fourier "
                "route must contract exponentially many terms implicitly, with "
                "polynomial circuit size, norm, precision, and witness extraction."
            ),
        },
        status=(
            "full-label-adaptive-polynomially-sparse-character-routes-obstructed"
        ),
        summary=(
            "Proved a source-uniform adaptive sparse-character obstruction, "
            f"verified {metrics['exact_fourier_target_count']} exact Fourier "
            f"targets with {control_failures} failures, and instantiated "
            f"{len(rows)} finite scaling rows. Dense implicit contractions remain open."
        ),
        falsifiers_triggered=[
            "Choosing sparse frequencies after seeing all public labels does not evade the simultaneous character-product bound.",
            "Low-order characters are usually annihilated exactly, not merely small on average.",
            "Polynomially many high-order characters cannot approximate the target-dependent fiber fluctuation.",
            "The zero-frequency term supplies only the target-independent mean fiber count.",
            "The theorem cannot be cited against a polynomial-size circuit that contracts exponentially many frequencies implicitly.",
        ],
    )


def write_sparse_character_obstruction(
    path: Path = DCP_SUBSET_SUM_SPARSE_CHARACTER_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: object,
) -> dict[str, object]:
    payload = asdict(run_sparse_character_obstruction(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    print(
        json.dumps(
            write_sparse_character_obstruction()["headline_metrics"],
            indent=2,
            sort_keys=True,
        )
    )
