"""Prime-power central cancellation controls, not an HSP receiver.

The scalar finite-field solver remains a published external dependency.
This module plans batches, verifies/lifts supplied scalar witnesses, and
counts a conservative retry tree under the stated IDEAL source promise.
Primality and genuine Lie/source contracts are not certified here.
"""
from dataclasses import dataclass
from fractions import Fraction
from math import gcd, prod
from typing import Sequence

from theorems.uniform_bch_rees import lift_scalar_witness


def _contract(prime, exponent, degree):
    if type(prime) is not int or prime < 3:
        raise ValueError("a supplied verified odd prime is required")
    if type(exponent) is not int or exponent < 1:
        raise ValueError("positive exponent required")
    if type(degree) is not int or not 1 <= degree < prime:
        raise ValueError("require 1 <= degree < prime")


def _valuation(value, prime):
    valuation = 0
    while value % prime == 0:
        valuation += 1
        value //= prime
    return valuation


@dataclass(frozen=True)
class BatchPlan:
    action: str
    valuation: int | None = None
    field_labels: tuple[int, ...] = ()
    zero_witness: tuple[int, ...] = ()


def plan_batch(labels: Sequence[int], *, prime: int, exponent: int, degree: int) -> BatchPlan:
    """Accept a zero label or one equal-valuation batch; otherwise retry.

    All batch inputs were already consumed. A retry is NOT a proof that
    no other unit-scale witness exists for the mixed-valuation labels.
    """
    _contract(prime, exponent, degree)
    labels = tuple(labels)
    modulus = prime**exponent
    if len(labels) != gcd(degree, prime-1) + 1:
        raise ValueError("the scalar power-index arity is required")
    if any(type(x) is not int or not 0 <= x < modulus for x in labels):
        raise ValueError("canonical labels modulo the stated prime power required")
    if 0 in labels:
        index = labels.index(0)
        return BatchPlan("zero", zero_witness=tuple(int(i == index) for i in range(len(labels))))
    valuations = tuple(_valuation(x, prime) for x in labels)
    if len(set(valuations)) != 1:
        return BatchPlan("retry")
    valuation = valuations[0]
    return BatchPlan("hensel", valuation,
                     tuple((x // prime**valuation) % prime for x in labels))


def lift_batch_witness(
    labels: Sequence[int], field_witness: Sequence[int], *,
    prime: int, exponent: int, degree: int,
) -> tuple[int, ...]:
    """Verify a reduced-degree field witness, then lift one unit coordinate.

    The supplied witness solves degree gcd(d,p-1) on the normalized labels.
    No search over the field or prime-power ring is performed. Active scales
    remain units; inactive scales remain EXACT zero, never nonzero nonunits.
    """
    labels = tuple(labels)
    plan = plan_batch(labels, prime=prime, exponent=exponent, degree=degree)
    if plan.action != "hensel":
        raise ValueError("equal-valuation nonzero batch required for Hensel lifting")
    scales = list(lift_scalar_witness(plan.field_labels, field_witness,
                                     prime=prime, degree=degree))
    normalized = tuple(x // prime**plan.valuation for x in labels)
    pivot = next(i for i, x in enumerate(scales) if x)
    derivative = normalized[pivot] * degree * pow(scales[pivot], degree-1, prime) % prime
    inverse = pow(derivative, -1, prime)
    power = prime
    for _ in range(1, exponent - plan.valuation):
        next_power = power * prime
        residual = sum(a * pow(x, degree, next_power)
                       for a, x in zip(normalized, scales)) % next_power
        if residual % power:
            raise ArithmeticError("Hensel invariant failed")
        correction = -(residual // power) * inverse % prime
        scales[pivot] += correction * power
        power = next_power
    if (not any(scales) or any(x and x % prime == 0 for x in scales)
            or sum(a * pow(x, degree, prime**exponent)
                   for a, x in zip(labels, scales)) % (prime**exponent)):
        raise ArithmeticError("invalid lifted unit-scale witness")
    return tuple(scales)


def batch_success_probability(*, prime: int, exponent: int, degree: int,
                              intersection_exponent: int) -> Fraction:
    """Exact IDEAL acceptance probability when |H intersect Z|=p**b.

    This probability assumes fresh independent uniform characters on K^perp.
    It neither infers b nor certifies a physical source from label marginals.
    """
    _contract(prime, exponent, degree)
    b = intersection_exponent
    if type(b) is not int or not 0 <= b <= exponent:
        raise ValueError("intersection exponent must lie between zero and exponent")
    if b == exponent:
        return Fraction(1)
    length = exponent - b
    arity = gcd(degree, prime-1) + 1
    zero = 1 - (1 - Fraction(1, prime**length))**arity
    same_nonzero = (Fraction((prime-1)**arity, prime**arity-1)
                    * (1 - Fraction(1, prime**(length*arity))))
    return zero + same_nonzero


def retry_tree_budget(*, prime: int, nilpotency_class: int,
                      higher_grade_cyclic_ranks: Sequence[int], terminal_samples: int) -> dict:
    """Conservative EXPECTATION and per-run Markov cap, not a measured run.

    Each cyclic factor has per-attempt acceptance at least1/4. A whole-run
    cap at16 times the expected leaf bound fails with probability <=1/16.
    Do not instead truncate every node at constant retries: there can be
    exponentially many nodes. Exponent sizes affect public arithmetic, not
    the number of copies in this bound. Profile checks are only necessary.
    """
    _contract(prime, 1, nilpotency_class)
    ranks = tuple(higher_grade_cyclic_ranks)
    if len(ranks) != nilpotency_class-1 or any(type(r) is not int or r < 1 for r in ranks):
        raise ValueError("one positive cyclic rank per actual higher grade required")
    if any(a < b for a, b in zip(ranks, ranks[1:])):
        raise ValueError("cyclic ranks of nested finite abelian p-groups cannot increase")
    if type(terminal_samples) is not int or terminal_samples < 1:
        raise ValueError("positive integer terminal count required")
    factor = prod((4*(gcd(d, prime-1)+1))**r for d, r in enumerate(ranks, start=2))
    mean = terminal_samples * factor
    cap = 16 * mean
    return {
        "cyclic_stages": sum(ranks),
        "expected_lifted_leaves_upper": mean,
        "expected_original_inputs_upper": nilpotency_class*mean,
        "hard_lifted_leaf_cap": cap,
        "hard_original_input_cap": nilpotency_class*cap,
        "full_instrument_cap": 2*cap + terminal_samples,
        "clock_failure_upper": "1/16",
        "status": "conditional_bound_not_receiver_execution",
    }
