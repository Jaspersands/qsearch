"""Conditional signed-L2 obstruction for low-bit subset-sum observables.

Write each random label as ``a_i = ell_i + 2^b h_i`` with exposed low part
``ell_i`` and unseen high part ``h_i`` uniform in ``Z_Q``,
``Q=2^(n-b)``.  Fix the low data and target.  Every low-compatible nonzero
Boolean assignment ``x`` has a carry-adjusted high equation

    <h, x> = r_x (mod Q).

For distinct nonzero Boolean assignments ``x`` and ``y``, their two-row binary
matrix contains a 2x2 minor of determinant ``+/-1``.  The map
``h -> (<h,x>, <h,y>)`` is therefore onto ``Z_Q^2``.  The exact-hit indicators
are pairwise independent even when ``r_x != r_y``.

Consequently, for arbitrary real/rational coefficients chosen from the exposed
low data and target, but not from the unseen high labels, let

    T = sum_x c_x 1[<h,x>=r_x]
    S = T - E[T | low data, target].

has conditional mean zero and exact conditional variance

    Var(S | low data, target) = (1/Q)(1-1/Q) sum_x c_x^2.

The uncentered score ``T`` remains at its no-hit baseline zero unless one of
the supported equations hits, an event of probability at most ``M/Q``.
Equivalently, ``S`` remains at the deterministic centered no-hit baseline
``-E[T | low data,target]`` outside that event.  Thus every fixed-polynomial
sparse signed exact-hit statistic of this type has negligible probability of a
high-label-dependent deviation when ``b=O(log n)``.  The theorem does not cover
coefficients that inspect the high labels, dense implicit contractions,
nonlinear statistics, or reduced-basis events.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Sequence

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_SIGNED_L2_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_signed_l2_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-SIGNED-L2-OBSTRUCTION"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class SignedL2TheoremCertificate:
    decomposition: str
    coefficient_access: str
    compatible_assignment_family: str
    unit_minor_lemma_proved: bool
    conditional_pairwise_independence_proved: bool
    conditional_centered_mean_formula: str
    conditional_variance_formula: str
    polynomial_support_nonbaseline_deviation_bound: str
    fixed_polynomial_support_negligible_deviation_proved: bool
    proof: str
    limitations: list[str]


@dataclass(frozen=True)
class ExactSignedL2Control:
    modulus_bits: int
    low_bits: int
    high_modulus: int
    register_count: int
    compatible_nonzero_assignment_count: int
    assignment_pair_count: int
    high_label_tuple_count: int
    marginal_probability: str
    expected_joint_probability: str
    marginal_uniformity_failure_count: int
    pairwise_independence_failure_count: int
    centered_mean: str
    expected_centered_mean: str
    centered_variance: str
    expected_centered_variance: str
    mean_identity_verified: bool
    variance_identity_verified: bool


@dataclass(frozen=True)
class SignedL2ScalingRow:
    n_bits: int
    exposed_low_bits: int
    high_modulus_bits: int
    support_power: int
    log2_support_upper_bound: float
    log2_nonbaseline_deviation_probability_upper_bound: float
    nonbaseline_deviation_probability_upper_bound: float
    inverse_polynomial_coverage_ruled_out_asymptotically: bool
    finite_row_is_computational_lower_bound: bool


@dataclass(frozen=True)
class DCPSubsetSumSignedL2Report:
    created_at: str
    theorem_contract: dict[str, str]
    theorem_certificate: SignedL2TheoremCertificate
    exact_controls: list[ExactSignedL2Control]
    rows: list[SignedL2ScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def unit_minor_columns(
    left: Sequence[int],
    right: Sequence[int],
) -> tuple[int, int]:
    """Return columns whose 2x2 determinant is a unit."""
    if len(left) != len(right) or not left:
        raise ValueError("assignment dimensions differ or are empty")
    if any(value not in {0, 1} for value in (*left, *right)):
        raise ValueError("assignments must be Boolean")
    if left == right or not any(left) or not any(right):
        raise ValueError("assignments must be distinct and nonzero")
    differing = next(
        index
        for index, (a, b) in enumerate(zip(left, right))
        if a != b
    )
    if left[differing] == 1:
        partner = next(index for index, value in enumerate(right) if value)
    else:
        partner = next(index for index, value in enumerate(left) if value)
    determinant = (
        left[differing] * right[partner]
        - left[partner] * right[differing]
    )
    if abs(determinant) != 1:
        raise AssertionError("constructed Boolean minor is not a unit")
    return differing, partner


def compatible_assignments_and_residues(
    low_labels: Sequence[int],
    target_low: int,
    target_high: int,
    low_bits: int,
    high_modulus: int,
) -> list[tuple[tuple[int, ...], int]]:
    if low_bits < 1 or high_modulus < 2:
        raise ValueError("invalid low/high moduli")
    low_modulus = 1 << low_bits
    if any(not 0 <= int(value) < low_modulus for value in low_labels):
        raise ValueError("low label lies outside its modulus")
    rows = []
    for assignment in itertools.product((0, 1), repeat=len(low_labels)):
        if not any(assignment):
            continue
        low_sum = sum(
            int(label) * bit
            for label, bit in zip(low_labels, assignment)
        )
        if low_sum % low_modulus != target_low % low_modulus:
            continue
        carry = (low_sum - (target_low % low_modulus)) // low_modulus
        rows.append(
            (
                assignment,
                (target_high - carry) % high_modulus,
            )
        )
    return rows


def _dot_mod(
    labels: Sequence[int],
    assignment: Sequence[int],
    modulus: int,
) -> int:
    return sum(
        int(label) * bit for label, bit in zip(labels, assignment)
    ) % modulus


def exact_signed_l2_control(
    modulus_bits: int = 3,
    low_bits: int = 1,
    low_labels: Sequence[int] = (1, 1, 0, 1),
    target_low: int = 0,
    target_high: int = 1,
) -> ExactSignedL2Control:
    if not 0 < low_bits < modulus_bits:
        raise ValueError("low bits must lie strictly inside the modulus")
    high_modulus = 1 << (modulus_bits - low_bits)
    equations = compatible_assignments_and_residues(
        low_labels,
        target_low,
        target_high,
        low_bits,
        high_modulus,
    )
    if len(equations) < 2:
        raise ArithmeticError("control needs at least two compatible assignments")
    for (left, _), (right, _) in itertools.combinations(equations, 2):
        unit_minor_columns(left, right)

    high_tuples = list(
        itertools.product(
            range(high_modulus), repeat=len(low_labels)
        )
    )
    marginal_expected = Fraction(1, high_modulus)
    joint_expected = marginal_expected * marginal_expected
    marginal_failures = 0
    for assignment, residue in equations:
        marginal_count = sum(
            _dot_mod(high, assignment, high_modulus) == residue
            for high in high_tuples
        )
        if Fraction(marginal_count, len(high_tuples)) != marginal_expected:
            marginal_failures += 1
    pair_failures = 0
    for (left, left_residue), (right, right_residue) in itertools.combinations(
        equations, 2
    ):
        joint_count = sum(
            _dot_mod(high, left, high_modulus) == left_residue
            and _dot_mod(high, right, high_modulus) == right_residue
            for high in high_tuples
        )
        if Fraction(joint_count, len(high_tuples)) != joint_expected:
            pair_failures += 1

    coefficients = [
        Fraction((index % 3) + 1)
        * (-1 if sum(assignment) % 2 else 1)
        for index, (assignment, _) in enumerate(equations)
    ]
    values = []
    for high in high_tuples:
        value = Fraction(0)
        for coefficient, (assignment, residue) in zip(
            coefficients, equations
        ):
            indicator = int(
                _dot_mod(high, assignment, high_modulus) == residue
            )
            value += coefficient * (indicator - marginal_expected)
        values.append(value)
    mean = sum(values, Fraction(0)) / len(values)
    variance = (
        sum(
            ((value - mean) ** 2 for value in values),
            Fraction(0),
        )
        / len(values)
    )
    expected_variance = (
        marginal_expected
        * (1 - marginal_expected)
        * sum(
            (coefficient * coefficient for coefficient in coefficients),
            Fraction(0),
        )
    )
    return ExactSignedL2Control(
        modulus_bits=modulus_bits,
        low_bits=low_bits,
        high_modulus=high_modulus,
        register_count=len(low_labels),
        compatible_nonzero_assignment_count=len(equations),
        assignment_pair_count=math.comb(len(equations), 2),
        high_label_tuple_count=len(high_tuples),
        marginal_probability=str(marginal_expected),
        expected_joint_probability=str(joint_expected),
        marginal_uniformity_failure_count=marginal_failures,
        pairwise_independence_failure_count=pair_failures,
        centered_mean=str(mean),
        expected_centered_mean="0",
        centered_variance=str(variance),
        expected_centered_variance=str(expected_variance),
        mean_identity_verified=mean == 0,
        variance_identity_verified=variance == expected_variance,
    )


def theorem_certificate() -> SignedL2TheoremCertificate:
    return SignedL2TheoremCertificate(
        decomposition=(
            "a_i=ell_i+2^b h_i with h_i independent uniform in "
            "Z_(2^(n-b)) after conditioning on all low labels"
        ),
        coefficient_access=(
            "c_x may depend arbitrarily on exposed low labels and the target "
            "but not on unseen high labels"
        ),
        compatible_assignment_family=(
            "all nonzero Boolean x whose low sum matches the target low residue; "
            "each x keeps its own exact carry-adjusted high right-hand side"
        ),
        unit_minor_lemma_proved=True,
        conditional_pairwise_independence_proved=True,
        conditional_centered_mean_formula="E[S | low,target]=0",
        conditional_variance_formula=(
            "Var(S | low,target)=Q^-1(1-Q^-1) sum_x c_x^2"
        ),
        polynomial_support_nonbaseline_deviation_bound=(
            "Pr[T != 0 | low,target] = "
            "Pr[S != -E[T|low,target] | low,target] <= |supp(c)|/Q"
        ),
        fixed_polynomial_support_negligible_deviation_proved=True,
        proof=(
            "For distinct nonzero Boolean x,y, choose a coordinate where they "
            "differ and a coordinate in the support of the row having zero at "
            "the first coordinate. The resulting 2x2 minor has determinant "
            "+/-1, a unit modulo every power of two. Hence the pair of high "
            "linear forms is exactly uniform on Z_Q^2 for arbitrary right-hand "
            "sides. Centered hit indicators have zero covariance. Expanding the "
            "square of the centered score S gives the variance identity. The "
            "uncentered score T can differ from its no-hit baseline zero only "
            "if at least one supported equation hits, so the union bound gives "
            "M/Q; equivalently S differs from its deterministic centered no-hit "
            "baseline only on that event. For M<=n^a and b=O(log n), this is "
            "exp(-Omega(n)) for every fixed a."
        ),
        limitations=[
            "The zero assignment is excluded; its target-zero event is deterministic and handled separately.",
            "Coefficients may not inspect the unseen high labels.",
            "The theorem does not cover LLL/reduced-basis coefficients computed from full labels.",
            "Dense implicitly contractible coefficient vectors are not ruled out.",
            "Nonlinear, higher-order, and adaptive statistics are not ruled out.",
            "No computational lower bound or witness decoder follows.",
        ],
    )


def signed_l2_scaling_row(
    n_bits: int,
    support_power: int,
    log_multiplier: int = 1,
) -> SignedL2ScalingRow:
    if n_bits < 4 or support_power < 0 or log_multiplier < 1:
        raise ValueError("invalid scaling parameters")
    low_bits = min(
        n_bits - 1,
        math.ceil(log_multiplier * math.log2(n_bits)),
    )
    high_bits = n_bits - low_bits
    log2_support = support_power * math.log2(n_bits)
    log2_probability = min(0.0, log2_support - high_bits)
    return SignedL2ScalingRow(
        n_bits=n_bits,
        exposed_low_bits=low_bits,
        high_modulus_bits=high_bits,
        support_power=support_power,
        log2_support_upper_bound=log2_support,
        log2_nonbaseline_deviation_probability_upper_bound=log2_probability,
        nonbaseline_deviation_probability_upper_bound=math.exp2(
            log2_probability
        ),
        inverse_polynomial_coverage_ruled_out_asymptotically=True,
        finite_row_is_computational_lower_bound=False,
    )


def run_signed_l2_obstruction(
    n_values: Sequence[int] = (32, 64, 128, 256, 512),
    support_powers: Sequence[int] = (1, 2, 4, 8),
    log_multiplier: int = 1,
) -> DCPSubsetSumSignedL2Report:
    if not n_values or not support_powers:
        raise ValueError("nonempty scaling ranges are required")
    controls = [exact_signed_l2_control()]
    rows = [
        signed_l2_scaling_row(n_bits, power, log_multiplier)
        for n_bits in n_values
        for power in support_powers
    ]
    control_failures = sum(
        control.marginal_uniformity_failure_count
        + control.pairwise_independence_failure_count
        + (not control.mean_identity_verified)
        + (not control.variance_identity_verified)
        for control in controls
    )
    tail_n = max(n_values)
    tail_rows = [row for row in rows if row.n_bits == tail_n]
    metrics: dict[str, int | float] = {
        "exact_control_count": len(controls),
        "exact_high_label_tuple_count": sum(
            control.high_label_tuple_count for control in controls
        ),
        "exact_assignment_pair_count": sum(
            control.assignment_pair_count for control in controls
        ),
        "exact_control_failure_count": control_failures,
        "unit_minor_theorem_count": 1,
        "conditional_pairwise_independence_theorem_count": 1,
        "conditional_signed_variance_identity_theorem_count": 1,
        "polynomial_support_negligible_deviation_theorem_count": 1,
        "scaling_row_count": len(rows),
        "maximum_n_bits": tail_n,
        "maximum_support_power": max(support_powers),
        "maximum_tail_nonbaseline_deviation_probability_upper_bound": max(
            row.nonbaseline_deviation_probability_upper_bound
            for row in tail_rows
        ),
        "proved_high_label_adaptive_signed_obstruction_count": 0,
        "proved_dense_implicit_signed_obstruction_count": 0,
        "proved_nonlinear_signed_obstruction_count": 0,
        "polynomial_witness_decoder_count": 0,
    }
    return DCPSubsetSumSignedL2Report(
        created_at=utc_now(),
        theorem_contract={
            "source": (
                "uniform labels in Z_(2^n)^(n+c), independent uniform target, "
                "conditioned on arbitrary exposed low-label data"
            ),
            "observable": (
                "signed linear combination of exact high-equation hits over "
                "low-compatible nonzero Boolean assignments"
            ),
            "coefficient_measurability": (
                "coefficients are measurable before unseen high labels are revealed"
            ),
            "conclusion": (
                "exact conditional L2 identity and negligible probability of "
                "departing from the no-hit baseline for fixed-polynomial support"
            ),
        },
        theorem_certificate=theorem_certificate(),
        exact_controls=controls,
        rows=rows,
        headline_metrics=metrics,
        claim_gate={
            "exact_controls_pass": control_failures == 0,
            "low_only_sparse_signed_exact_hit_observables_closed": True,
            "high_label_adaptive_signed_observables_closed": False,
            "dense_implicit_signed_observables_closed": False,
            "nonlinear_signed_observables_closed": False,
            "reduced_basis_geometry_closed": False,
            "polynomial_witness_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Signed weights chosen only from low data cannot rescue a "
                "polynomial support: their exact-hit indicators are conditionally "
                "pairwise independent and the support departs from its no-hit "
                "baseline with negligible probability. Full-label adaptive or "
                "dense implicit observables remain open."
            ),
        },
        status=(
            "low-only-polynomial-support-signed-exact-hit-observables-asymptotically-obstructed"
        ),
        summary=(
            f"Proved the conditional signed-L2 identity and polynomial-support "
            f"nonbaseline-deviation obstruction, verified "
            f"{metrics['exact_assignment_pair_count']} "
            f"assignment pairs exactly, and instantiated {len(rows)} scaling "
            "rows. Full-label adaptive and dense implicit signed observables remain open."
        ),
        falsifiers_triggered=[
            "Changing signs cannot increase the probability that a polynomially supported low-only exact-hit score departs from its no-hit baseline.",
            "A finite signed exact-hit score selected from low data is governed by an exact conditional variance identity, not unexplained structure.",
            "Low-bit conditioning does not create covariance between distinct nonzero Boolean high-equation hits.",
            "The theorem cannot be cited against coefficients computed from full high labels, dense implicit contractions, or reduced-basis events.",
        ],
    )


def write_signed_l2_obstruction(
    path: Path = DCP_SUBSET_SUM_SIGNED_L2_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: object,
) -> dict[str, object]:
    payload = asdict(run_signed_l2_obstruction(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    print(
        json.dumps(
            write_signed_l2_obstruction()["headline_metrics"],
            indent=2,
            sort_keys=True,
        )
    )
