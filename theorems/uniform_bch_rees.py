"""Uniform BCH arithmetic and scalar-line Rees resource bounds.

These are public algebra/resource controls, NOT an HSP receiver or diagonal
equation solver. The caller supplies a genuine Lie bracket over a verified
prime field and a valid nilpotency-class bound below the characteristic.
Shape checks do not certify those mathematical promises. No field table,
free-Lie word expansion, hidden subgroup, or cloud-offloaded import is used.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from typing import Callable, Sequence


Vector = tuple[int, ...]
Bracket = Callable[[Vector, Vector], Sequence[int]]


def _field_contract(prime: int, nilpotency_class: int) -> None:
    if type(prime) is not int or prime < 2:
        raise ValueError("a supplied verified prime is required")
    if (type(nilpotency_class) is not int
            or not 1 <= nilpotency_class < prime):
        raise ValueError("require 1 <= nilpotency_class < prime")


def _vector(value: Sequence[int], dimension: int, prime: int) -> Vector:
    result = tuple(value)
    if len(result) != dimension or any(
        type(x) is not int or not 0 <= x < prime for x in result
    ):
        raise ValueError("canonical field vector of the stated dimension required")
    return result


def inverse_left_dexp_coefficients(prime: int, nilpotency_class: int) -> Vector:
    """Coefficients of z/(1-exp(-z)) modulo z**c, with c < prime.

    The inverse power-series recurrence only divides by integers at most c.
    Primality is an input promise, not inferred from invertible denominators.
    """
    _field_contract(prime, nilpotency_class)
    factorial = 1
    f = []
    for k in range(nilpotency_class):
        factorial = factorial * (k + 1) % prime
        f.append((-1)**k * pow(factorial, -1, prime) % prime)
    b = [1]
    for k in range(1, nilpotency_class):
        b.append(-sum(f[j] * b[k-j] for j in range(1, k+1)) % prime)
    return tuple(b)


def bch_via_ode(
    x: Sequence[int], y: Sequence[int], *, prime: int,
    nilpotency_class: int, bracket: Bracket,
) -> Vector:
    """Return log(exp(x) exp(y)) for the promised class-<p Lie algebra.

    Solve Z'=ad_Z/(1-exp(-ad_Z)) y, Z(0)=x, coefficientwise through
    degree c. Polynomial bracket convolution avoids enumerating Lie words.
    At most (c-1)*c*(c+1)*(c+2)/6 calls to the supplied bracket are made.
    An understated class or a non-Lie callback can give a wrong answer;
    callers must obtain the class from validated public structure constants.
    """
    coefficients = inverse_left_dexp_coefficients(prime, nilpotency_class)
    x = tuple(x)
    if not x:
        raise ValueError("positive vector dimension required")
    dimension = len(x)
    x, y = _vector(x, dimension, prime), _vector(y, dimension, prime)
    zero = (0,) * dimension
    z = [x]
    for degree in range(nilpotency_class):
        ad = [y] + [zero] * degree
        rhs = list(ad[degree])
        for power in range(1, nilpotency_class):
            next_ad = []
            for order in range(degree + 1):
                total = [0] * dimension
                for i in range(order + 1):
                    value = _vector(bracket(z[i], ad[order-i]), dimension, prime)
                    for j, entry in enumerate(value):
                        total[j] += entry
                next_ad.append(tuple(entry % prime for entry in total))
            ad = next_ad
            weight = coefficients[power]
            rhs = [(a + weight*b) % prime for a, b in zip(rhs, ad[degree])]
        inverse = pow(degree + 1, -1, prime)
        z.append(tuple(inverse * entry % prime for entry in rhs))
    return tuple(sum(row[i] for row in z) % prime for i in range(dimension))


def lift_scalar_witness(
    labels: Sequence[int], witness: Sequence[int], *, prime: int, degree: int,
) -> Vector:
    """Check a gcd(d,p-1)-power witness and lift it to a d-power witness.

    This verifies/converts an existing witness; it does not find one.
    Zero entries stay zero, even when the reduced exponent inverse is zero.
    """
    _field_contract(prime, degree)
    labels = tuple(labels)
    labels = _vector(labels, len(labels), prime)
    witness = _vector(witness, len(labels), prime)
    delta = gcd(degree, prime-1)
    if not any(witness) or sum(a*pow(x, delta, prime) for a, x in zip(labels, witness)) % prime:
        raise ValueError("a nonzero valid reduced-power witness is required")
    exponent = pow(degree // delta, -1, (prime-1) // delta)
    return tuple(pow(x, exponent, prime) if x else 0 for x in witness)


@dataclass(frozen=True)
class ScalarLineStage:
    grade: int
    line: int
    arity: int
    conversions: int
    consumed_targets: int


@dataclass(frozen=True)
class ScalarLineBudget:
    lower_central_dimensions: tuple[int, ...]
    terminal_samples: int
    prime: int | None
    cover_dimension: int
    lifted_sources: int
    original_inputs: int
    scalar_solves: int
    central_character_measurements: int
    stages: tuple[ScalarLineStage, ...]

    @property
    def derived_dimension(self) -> int:
        return self.lower_central_dimensions[1] if len(self.lower_central_dimensions) > 1 else 0

    @property
    def leaves_per_terminal(self) -> int:
        return self.lifted_sources // self.terminal_samples

    @property
    def derived_parameter_leaf_bound(self) -> int:
        r = self.derived_dimension
        return (r + 2)**(r * (r + 1) // 2)


def scalar_line_budget(
    lower_central_dimensions: Sequence[int], terminal_samples: int, *, prime: int | None = None,
) -> ScalarLineBudget:
    """Worst-case fresh-source tree, using d+1 inputs per grade-d line.

    The profile is (dim L, dim gamma_2, ..., dim gamma_c), without trailing
    zeros. Necessary profile checks are not a Lie-algebra existence proof.
    Each conversion calls a published scalar diagonal solver once and
    consumes/measures ALL its d+1 targets, including zero-scale branches.
    With a supplied verified prime, arity is gcd(d,p-1)+1 instead of d+1.
    Initial lift calls consume c ordinary f queries OR c original copies.
    State preparation, gates, final Fourier sampling and errors remain paid
    separately; this function does not claim to count them as scalar solves.
    """
    dimensions = tuple(lower_central_dimensions)
    if not dimensions or any(type(x) is not int or x < 1 for x in dimensions):
        raise ValueError("positive lower-central dimensions without trailing zero required")
    if any(a <= b for a, b in zip(dimensions, dimensions[1:])):
        raise ValueError("nonzero lower-central dimensions must strictly decrease")
    if len(dimensions) > 1 and dimensions[0] - dimensions[1] < 2:
        raise ValueError("nonabelian nilpotent Lie algebra needs abelianization dimension >= 2")
    if type(terminal_samples) is not int or terminal_samples < 1:
        raise ValueError("positive integer terminal sample count required")
    if prime is not None:
        _field_contract(prime, len(dimensions))
    need = terminal_samples
    stages = []
    # Work backward from the final quotient; never reuse a consumed target.
    for grade, rank in enumerate(dimensions[1:], start=2):
        arity = gcd(grade, prime-1) + 1 if prime is not None else grade + 1
        for line in range(rank - 1, -1, -1):
            consumed = arity * need
            stages.append(ScalarLineStage(grade, line, arity, need, consumed))
            need = consumed
    stages.reverse()
    return ScalarLineBudget(
        dimensions, terminal_samples, prime, sum(dimensions), need,
        len(dimensions) * need, sum(stage.conversions for stage in stages),
        sum(stage.consumed_targets for stage in stages), tuple(stages),
    )
