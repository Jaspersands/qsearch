"""Affine-invariant ANF-degree obstruction for 2-adic subset-sum carries.

For ``S(x)=sum_i a_i x_i`` and output bit ``j``, Lucas' theorem gives

    bit_j(S(x)) = binom(S(x), 2^j) mod 2.

In the Boolean function ring, its algebraic-normal-form coefficient on a
variable set ``I`` is

    [z^(2^j)] product_(i in I) ((1+z)^(a_i)-1) mod 2.       (1)

Every nonconstant factor in (1) has minimum degree at least one, so the ANF
degree is at most ``2^j``.  If at least ``2^j`` labels are odd, every set of
``2^j`` odd labels contributes coefficient one: only the product of their
linear ``z`` terms can reach total degree ``2^j``.  The degree is therefore
exactly ``2^j`` and at least ``binom(O,2^j)`` top-degree monomials occur, where
``O`` is the number of odd labels.

With ``m=q+O(1)`` random labels, choose the largest power of two at most
``m/6``.  A Chernoff bound gives ``O>=floor(m/3)`` except with probability at
most ``exp(-m/36)``.  Consequently a linear-degree carry predicate with
exponentially many top monomials occurs with exponentially high probability.
Algebraic degree is invariant under every invertible affine change of Boolean
variables, so even a dense ``GL(m,2)`` preprocessing cannot make all carry
constraints bounded degree in the transformed variables.

This is only an obstruction to bounded-degree ANF reconstruction in the
original variable count.  It is not a subset-sum lower bound and does not
exclude auxiliary variables, arithmetic circuits, tensor contractions,
implicit quantum walks, or a polynomial density-one subset-sum solver.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

from dcp_subset_sum_carry_anf import anf_coefficients
from research_registry import utc_now


REPORT_PATH = Path(
    "research/classical_baselines/dcp_carry_affine_degree_invariance.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-CARRY-AFFINE-DEGREE-INVARIANCE"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class CarryCoefficientControl:
    modulus_bits: int
    labels: tuple[int, ...]
    output_bit: int
    target_bit: int
    odd_label_count: int
    degree_ceiling: int
    exact_anf_degree: int
    exact_top_degree_monomial_count: int
    odd_top_monomial_lower_bound: int
    generating_function_coefficient_failure_count: int
    lucas_truth_identity_failure_count: int
    exact_degree_theorem_applicable: bool
    exact_degree_theorem_verified: bool
    status: str


@dataclass(frozen=True)
class AffineDegreeInvarianceControl:
    variable_count: int
    modulus_bits: int
    output_bit: int
    linear_rows: tuple[int, ...]
    translation_mask: int
    linear_rank: int
    original_degree: int
    transformed_degree: int
    degree_preserved: bool
    status: str


@dataclass(frozen=True)
class CarryAffineDegreeScalingRecord:
    modulus_bits: int
    register_offset: int
    register_count: int
    selected_output_bit: int
    certified_anf_degree: int
    certified_degree_fraction: float
    odd_label_threshold: int
    top_degree_monomial_log2_lower_bound: float
    high_degree_failure_probability_log2_upper_bound: float
    affine_invariant_linear_degree_certified: bool
    bounded_degree_after_dense_gl_ruled_out: bool
    status: str


@dataclass(frozen=True)
class CarryAffineDegreeTheorem:
    lucas_bit_identity: str
    anf_coefficient_formula: str
    exact_degree_condition: str
    random_label_consequence: str
    affine_invariance: str
    obstruction_scope: str
    lucas_identity_proved: bool
    coefficient_formula_proved: bool
    linear_degree_with_exponentially_many_terms_proved: bool
    arbitrary_invertible_affine_degree_reduction_ruled_out: bool
    auxiliary_variable_reformulation_ruled_out: bool
    tensor_rank_collapse_ruled_out: bool
    polynomial_subset_sum_solver_ruled_out: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class DCPCarryAffineDegreeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    coefficient_controls: list[CarryCoefficientControl]
    affine_controls: list[AffineDegreeInvarianceControl]
    scaling_records: list[CarryAffineDegreeScalingRecord]
    theorem: CarryAffineDegreeTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _gf2_rank(rows: Sequence[int], width: int) -> int:
    basis: dict[int, int] = {}
    mask = (1 << width) - 1
    for raw in rows:
        value = int(raw) & mask
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def _anf_degree(coefficients: Sequence[int | bool]) -> int:
    active = [
        mask for mask, coefficient in enumerate(coefficients) if coefficient
    ]
    return max((mask.bit_count() for mask in active), default=0)


def carry_truth_table(
    labels: Sequence[int],
    output_bit: int,
    target_bit: int = 0,
) -> bytearray:
    if output_bit < 0 or target_bit not in (0, 1):
        raise ValueError("invalid output or target bit")
    canonical = tuple(int(label) for label in labels)
    if not canonical or any(label < 0 for label in canonical):
        raise ValueError("labels must be nonnegative and nonempty")
    return bytearray(
        (((sum(
            canonical[index]
            for index in range(len(canonical))
            if (assignment >> index) & 1
        ) >> output_bit) & 1) ^ target_bit)
        for assignment in range(1 << len(canonical))
    )


def lucas_bit_from_binomial(value: int, output_bit: int) -> int:
    """Evaluate Lucas' bit identity directly for finite exact controls."""

    if value < 0 or output_bit < 0:
        raise ValueError("value and output_bit must be nonnegative")
    return math.comb(value, 1 << output_bit) & 1


def carry_anf_coefficient_from_generating_function(
    labels: Sequence[int],
    output_bit: int,
    variable_mask: int,
) -> int:
    """Return one coefficient from formula (1), truncated at ``2^j``."""

    degree = 1 << output_bit
    if variable_mask < 0 or variable_mask >= 1 << len(labels):
        raise ValueError("variable mask is out of range")
    polynomial = bytearray(degree + 1)
    polynomial[0] = 1
    for index, raw_label in enumerate(labels):
        if not (variable_mask >> index) & 1:
            continue
        label = int(raw_label)
        if label < 0:
            raise ValueError("labels must be nonnegative")
        exponents = []
        subset = label
        while subset:
            if subset <= degree:
                exponents.append(subset)
            subset = (subset - 1) & label
        updated = bytearray(degree + 1)
        for left, coefficient in enumerate(polynomial):
            if not coefficient:
                continue
            for right in exponents:
                if left + right <= degree:
                    updated[left + right] ^= 1
        polynomial = updated
    return int(polynomial[degree])


def audit_carry_coefficient_identity(
    labels: Sequence[int],
    output_bit: int,
    *,
    target_bit: int = 0,
) -> CarryCoefficientControl:
    canonical = tuple(int(label) for label in labels)
    if not canonical:
        raise ValueError("labels must be nonempty")
    modulus_bits = max(1, max(canonical).bit_length(), output_bit + 1)
    truth = carry_truth_table(canonical, output_bit, target_bit)
    coefficients = anf_coefficients(truth, len(canonical))
    formula_failures = 0
    for variable_mask, coefficient in enumerate(coefficients):
        predicted = carry_anf_coefficient_from_generating_function(
            canonical,
            output_bit,
            variable_mask,
        )
        if variable_mask == 0 and target_bit:
            predicted ^= 1
        formula_failures += int(predicted != coefficient)
    lucas_failures = 0
    for assignment, truth_value in enumerate(truth):
        total = sum(
            canonical[index]
            for index in range(len(canonical))
            if (assignment >> index) & 1
        )
        predicted = lucas_bit_from_binomial(total, output_bit) ^ target_bit
        lucas_failures += int(predicted != truth_value)
    ceiling = 1 << output_bit
    degree = _anf_degree(coefficients)
    top_count = sum(
        bool(coefficient) and mask.bit_count() == degree
        for mask, coefficient in enumerate(coefficients)
    )
    odd_count = sum(label & 1 for label in canonical)
    applicable = odd_count >= ceiling
    lower_bound = math.comb(odd_count, ceiling) if applicable else 0
    verified = (
        formula_failures == 0
        and lucas_failures == 0
        and degree <= ceiling
        and (
            not applicable
            or (degree == ceiling and top_count >= lower_bound)
        )
    )
    return CarryCoefficientControl(
        modulus_bits=modulus_bits,
        labels=canonical,
        output_bit=output_bit,
        target_bit=target_bit,
        odd_label_count=odd_count,
        degree_ceiling=ceiling,
        exact_anf_degree=degree,
        exact_top_degree_monomial_count=top_count,
        odd_top_monomial_lower_bound=lower_bound,
        generating_function_coefficient_failure_count=formula_failures,
        lucas_truth_identity_failure_count=lucas_failures,
        exact_degree_theorem_applicable=applicable,
        exact_degree_theorem_verified=verified,
        status=(
            "lucas-generating-function-degree-theorem-verified"
            if verified
            else "carry-coefficient-control-failure"
        ),
    )


def audit_affine_degree_invariance(
    labels: Sequence[int],
    output_bit: int,
    linear_rows: Sequence[int],
    translation_mask: int = 0,
) -> AffineDegreeInvarianceControl:
    """Verify degree preservation for one explicit invertible affine map.

    ``linear_rows[i]`` describes original variable ``x_i`` as a parity of the
    transformed variables ``z``.  ``translation_mask`` supplies the affine
    constant of each original coordinate.
    """

    canonical = tuple(int(label) for label in labels)
    variable_count = len(canonical)
    rows = tuple(int(row) for row in linear_rows)
    if len(rows) != variable_count:
        raise ValueError("the affine map needs one row per variable")
    rank = _gf2_rank(rows, variable_count)
    if rank != variable_count:
        raise ValueError("the linear part must be invertible")
    if not 0 <= translation_mask < 1 << variable_count:
        raise ValueError("translation mask is out of range")
    original_truth = carry_truth_table(canonical, output_bit)
    transformed_truth = bytearray(1 << variable_count)
    for transformed in range(1 << variable_count):
        original = 0
        for index, row in enumerate(rows):
            bit = ((row & transformed).bit_count() & 1) ^ (
                (translation_mask >> index) & 1
            )
            original |= bit << index
        transformed_truth[transformed] = original_truth[original]
    original_degree = _anf_degree(
        anf_coefficients(original_truth, variable_count)
    )
    transformed_degree = _anf_degree(
        anf_coefficients(transformed_truth, variable_count)
    )
    preserved = original_degree == transformed_degree
    return AffineDegreeInvarianceControl(
        variable_count=variable_count,
        modulus_bits=max(1, max(canonical).bit_length()),
        output_bit=output_bit,
        linear_rows=rows,
        translation_mask=translation_mask,
        linear_rank=rank,
        original_degree=original_degree,
        transformed_degree=transformed_degree,
        degree_preserved=preserved,
        status=(
            "invertible-affine-anf-degree-preserved"
            if preserved
            else "affine-degree-invariance-control-failure"
        ),
    )


def selected_linear_degree(register_count: int) -> tuple[int, int]:
    """Choose ``2^j`` in ``(m/12,m/6]`` for the random-label theorem."""

    if register_count < 24:
        raise ValueError("register_count must be at least twenty-four")
    degree = 1 << math.floor(math.log2(register_count / 6))
    return degree.bit_length() - 1, degree


def _log2_binomial(population: int, selections: int) -> float:
    if not 0 <= selections <= population:
        raise ValueError("invalid binomial parameters")
    return (
        math.lgamma(population + 1)
        - math.lgamma(selections + 1)
        - math.lgamma(population - selections + 1)
    ) / math.log(2)


def carry_affine_degree_scaling_record(
    modulus_bits: int,
    *,
    register_offset: int = 4,
) -> CarryAffineDegreeScalingRecord:
    if modulus_bits < 20:
        raise ValueError("modulus_bits must be at least twenty")
    register_count = modulus_bits + register_offset
    output_bit, degree = selected_linear_degree(register_count)
    if output_bit >= modulus_bits:
        raise ValueError("selected output bit must lie below the modulus")
    odd_threshold = register_count // 3
    if degree > odd_threshold:
        raise AssertionError("degree schedule exceeds the odd-label threshold")
    top_log = _log2_binomial(odd_threshold, degree)
    failure_log2 = -register_count / (36.0 * math.log(2))
    certified = (
        degree >= register_count / 12
        and degree <= register_count / 6
        and top_log > 0.05 * register_count
        and failure_log2 < 0
    )
    return CarryAffineDegreeScalingRecord(
        modulus_bits=modulus_bits,
        register_offset=register_offset,
        register_count=register_count,
        selected_output_bit=output_bit,
        certified_anf_degree=degree,
        certified_degree_fraction=degree / register_count,
        odd_label_threshold=odd_threshold,
        top_degree_monomial_log2_lower_bound=top_log,
        high_degree_failure_probability_log2_upper_bound=failure_log2,
        affine_invariant_linear_degree_certified=certified,
        bounded_degree_after_dense_gl_ruled_out=certified,
        status=(
            "random-carry-linear-degree-affine-invariant"
            if certified
            else "finite-scaling-not-yet-in-linear-degree-regime"
        ),
    )


def carry_affine_degree_theorem() -> CarryAffineDegreeTheorem:
    return CarryAffineDegreeTheorem(
        lucas_bit_identity=(
            "bit_j(s)=binom(s,2^j) mod 2 for every nonnegative integer s"
        ),
        anf_coefficient_formula=(
            "hat f(I)=[z^(2^j)] product_(i in I)((1+z)^a_i-1) over F_2"
        ),
        exact_degree_condition=(
            "if O labels are odd and O>=2^j, degree(f_j)=2^j and at "
            "least binom(O,2^j) top-degree monomials occur"
        ),
        random_label_consequence=(
            "for 2^j in (m/12,m/6], degree Theta(m) with exp(Omega(m)) "
            "top monomials except with probability exp(-m/36)"
        ),
        affine_invariance=(
            "deg(f composed with L)=deg(f) for every invertible affine L, "
            "by applying the degree upper bound to L and L inverse"
        ),
        obstruction_scope=(
            "bounded-degree ANF reconstruction after arbitrary dense affine "
            "Boolean preprocessing, without auxiliary variables"
        ),
        lucas_identity_proved=True,
        coefficient_formula_proved=True,
        linear_degree_with_exponentially_many_terms_proved=True,
        arbitrary_invertible_affine_degree_reduction_ruled_out=True,
        auxiliary_variable_reformulation_ruled_out=False,
        tensor_rank_collapse_ruled_out=False,
        polynomial_subset_sum_solver_ruled_out=False,
        theorem_verified=True,
        status="dense-affine-bounded-degree-carry-route-closed",
    )
