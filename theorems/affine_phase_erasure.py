"""Public polynomial-phase erasure on unknown parallel affine subspaces.

The coefficient routines are polynomial-size classical controllers. Sparse
state simulation enumerates field points and is ONLY a finite diagnostic.
No hidden direction, phase coefficients, or coset origin enters the controller.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import comb, sqrt
import random

from flint import nmod_mat
import numpy as np

from theorems.graded_hsp_phase_descent import _canonical, _dependence
from theorems.prime_character_opi import ring


@lru_cache(maxsize=None)
def monomials(width, degree):
    if type(width) is not int or width < 1 or type(degree) is not int or degree < 0:
        raise ValueError("positive width and nonnegative degree required")
    if width == 1:
        return tuple((i,) for i in range(degree + 1))
    return tuple((i,) + tail for i in range(degree + 1)
                 for tail in monomials(width - 1, degree - i))


def independent_columns(columns, p):
    """Compress equation rows, not source columns; preserve the exact kernel."""
    if not columns or not columns[0]:
        raise ValueError("nonempty coefficient columns required")
    for column in columns:
        _canonical(column, len(columns[0]), p)
    reduced, rank = nmod_mat(list(map(list, zip(*columns))), p).rref()
    if rank == 0:
        return [[0] for _ in columns], 0
    return [[int(reduced[j, i]) for j in range(rank)] for i in range(len(columns))], rank


def square_weights(p, columns, rng):
    """Known two-layer square-coefficient construction, p=3 mod 4.

    Split each linear relation into squares and negative squares. Two layers
    give four disjoint equal vector sums. A public isotropic ternary quadratic
    vector cancels three of them. The randomized conic search has mean <3.
    """
    ring(p)
    if p % 4 != 3:
        raise ValueError("square controller currently requires p=3 mod 4")
    columns, rank = independent_columns(columns, p)
    size = (rank + 1) ** 2
    if len(columns) < size:
        raise ValueError(f"square controller needs {size} columns at rank {rank}")
    if rank == 0:
        return [1] + [0] * (len(columns) - 1)

    def split(vectors):
        relation = _dependence(p, vectors)
        plus, minus = {}, {}
        for i, a in enumerate(relation):
            if a:
                target = plus if pow(a, (p - 1) // 2, p) == 1 else minus
                value = a if target is plus else -a % p
                target[i] = pow(value, (p + 1) // 4, p)
        value = [sum(vectors[i][j] * b * b for i, b in plus.items()) % p
                 for j in range(rank)]
        return plus, minus, value

    inner, values = [], []
    for start in range(0, size, rank + 1):
        plus, minus, value = split(columns[start:start + rank + 1])
        blocks = ({start + i: b for i, b in plus.items()},
                  {start + i: b for i, b in minus.items()})
        if not any(value):
            selected = blocks[0] or blocks[1]
            return [selected.get(i, 0) for i in range(len(columns))]
        inner.append(blocks)
        values.append(value)
    plus, minus, value = split(values)
    four = []
    for outer in (plus, minus):
        for side in (0, 1):
            four.append({i: b * scale % p for block, scale in outer.items()
                         for i, b in inner[block][side].items()})
    if not any(value):
        selected = next(block for block in four if block)
        return [selected.get(i, 0) for i in range(len(columns))]
    # Exactly (p+1)/2 choices of x make -1-x^2 a nonzero square for p=3 mod4.
    while True:
        x = rng.randrange(p)
        y2 = (-1 - x * x) % p
        if pow(y2, (p - 1) // 2, p) == 1:
            scales = (x, pow(y2, (p + 1) // 4, p), 1, 0)
            break
    result = [0] * len(columns)
    for block, scale in zip(four, scales):
        for i, b in block.items():
            result[i] = b * scale % p
    return result


@dataclass
class PhasePacket:
    """Public map beta -> coefficients of unknown fixed potential parameters."""

    p: int
    width: int
    parameter_count: int
    coefficients: dict[tuple[int, ...], tuple[int, ...]]

    def __post_init__(self):
        ring(self.p)
        if self.width < 1 or self.parameter_count < 1:
            raise ValueError("positive dimensions required")
        for alpha, vector in self.coefficients.items():
            if len(alpha) != self.width or not any(alpha) or any(type(a) is not int or a < 0 for a in alpha):
                raise ValueError("nonconstant canonical monomial required")
            _canonical(vector, self.parameter_count, self.p)
        self.coefficients = {a: v for a, v in self.coefficients.items() if any(v)}

    @property
    def degree(self):
        return max(map(sum, self.coefficients), default=0)

    def evaluate_fixture(self, point, parameters):
        """Diagnostic evaluation only; the controller never calls this."""
        _canonical(point, self.width, self.p)
        _canonical(parameters, self.parameter_count, self.p)
        return sum(sum(x * y for x, y in zip(vector, parameters)) *
                   np.prod([pow(x, a, self.p) for x, a in zip(point, alpha)], dtype=object)
                   for alpha, vector in self.coefficients.items()) % self.p


def initial_packet(p, width, label, max_degree=3):
    _canonical(label, len(label), p)
    if not label:
        raise ValueError("positive label dimension required")
    basis = [alpha for alpha in monomials(width, max_degree) if any(alpha)]
    count = len(basis) * len(label)
    coefficients = {}
    for j, alpha in enumerate(basis):
        row = [0] * count
        row[j * len(label):(j + 1) * len(label)] = label
        coefficients[alpha] = tuple(row)
    return PhasePacket(p, width, count, coefficients)


def leading_columns(packets, degree):
    first = packets[0]
    if any((v.p, v.width, v.parameter_count) !=
           (first.p, first.width, first.parameter_count) or v.degree > degree for v in packets):
        raise ValueError("compatible packets of bounded degree required")
    basis = [a for a in monomials(first.width, degree) if sum(a) == degree]
    zeros = (0,) * first.parameter_count
    return [tuple(x for alpha in basis for x in packet.coefficients.get(alpha, zeros))
            for packet in packets]


def cancellation_weights(packets, degree, rng=None):
    """Choose scales from public coefficient maps ONLY, never from amplitudes."""
    if degree not in (1, 2, 3):
        raise ValueError("implemented degrees are 1, 2, 3")
    p = packets[0].p
    columns = leading_columns(packets, degree)
    compressed, rank = independent_columns(columns, p)
    if not rank:
        weights = [1] + [0] * (len(packets) - 1)
    elif degree == 2:
        weights = square_weights(p, compressed, rng or random.Random(0))
    else:
        coefficients = _dependence(p, compressed)
        if degree == 3:
            if p % 3 != 2:
                raise ValueError("cubic controller currently requires p=2 mod3")
            coefficients = [pow(c, pow(3, -1, p - 1), p) for c in coefficients]
        weights = coefficients
    if not any(weights) or any(sum(column[j] * pow(c, degree, p)
                                   for column, c in zip(columns, weights)) % p
                               for j in range(len(columns[0]))):
        raise ArithmeticError("public leading-degree cancellation failed")
    return weights, rank


@lru_cache(maxsize=None)
def _submonomials(alpha):
    return tuple((beta, np.prod([comb(a, b) for a, b in zip(alpha, beta)], dtype=object))
                 for beta in product(*(range(a + 1) for a in alpha)) if any(beta))


def translate_combine(packets, weights, outcomes):
    """Update the symbolic phase after the public coordinate-shear measurement."""
    first = packets[0]
    if len(packets) != len(weights) or len(packets) != len(outcomes) or not any(weights):
        raise ValueError("matching packets, nonzero scales and outcomes required")
    _canonical(weights, len(weights), first.p)
    leading_columns(packets, max(v.degree for v in packets))
    result = {}
    for packet, c, y in zip(packets, weights, outcomes):
        _canonical(y, first.width, first.p)
        if not c:
            continue
        for alpha, vector in packet.coefficients.items():
            for beta, factor in _submonomials(alpha):
                scalar = int(factor) * pow(c, sum(beta), first.p)
                for yj, a, b in zip(y, alpha, beta):
                    scalar = scalar * pow(yj, a - b, first.p) % first.p
                if scalar:
                    row = result.setdefault(beta, [0] * first.parameter_count)
                    for j, value in enumerate(vector):
                        row[j] = (row[j] + scalar * value) % first.p
    return PhasePacket(first.p, first.width, first.parameter_count,
                       {a: tuple(v) for a, v in result.items()})


def merge_branch(p, states, weights, outcomes):
    """Finite simulation of one physical branch, without knowing the support line.

    Prepare |+> on Fp^m, subtract c_i*x from each source register, measure
    those registers. Zero-scale copies are discarded, not reused or cloned.
    """
    if not states or len(states) != len(weights) or len(states) != len(outcomes) or not any(weights):
        raise ValueError("matching states, nonzero scales and outcomes required")
    if any(not state for state in states):
        raise ValueError("nonempty source states required")
    width = len(next(iter(states[0])))
    _canonical(weights, len(weights), p)
    for y in outcomes:
        _canonical(y, width, p)
    active = [i for i, c in enumerate(weights) if c]
    i = active[0]
    inverse = pow(weights[i], -1, p)
    candidates = [tuple((qj - yj) * inverse % p for qj, yj in zip(q, outcomes[i]))
                  for q in states[i]]
    amplitudes = {}
    # Equal moduli are a precondition of the proved instrument. Work with
    # unit phases to avoid underflow for large batches, and charge norms below.
    for state in states:
        target = 1 / sqrt(len(state))
        if not state or any(abs(abs(a) - target) > 1e-9 for a in state.values()):
            raise ValueError("normalized equal-modulus sparse states required")
    for x in candidates:
        phase = 1 + 0j
        for j in active:
            q = tuple((yj + weights[j] * xj) % p for yj, xj in zip(outcomes[j], x))
            a = states[j].get(q)
            if a is None:
                break
            phase *= a / abs(a)
        else:
            amplitudes[x] = phase
    denominator = p ** width
    for j in active:
        denominator *= len(states[j])
    probability = Fraction(len(amplitudes), denominator)
    if not amplitudes:
        return {}, probability
    return {x: a / sqrt(len(amplitudes)) for x, a in amplitudes.items()}, probability


def sample_merge(p, states, packets, weights, rng):
    """Diagnostic Born sampler. No sample or branch is postselected."""
    width = packets[0].width
    fresh = tuple(rng.randrange(p) for _ in range(width))
    outcomes = []
    for state, c in zip(states, weights):
        if not c:
            outcomes.append((0,) * width)
            continue
        q = rng.choice(tuple(state))
        outcomes.append(tuple((qj - c * xj) % p for qj, xj in zip(q, fresh)))
    state, probability = merge_branch(p, states, weights, outcomes)
    if not state:
        raise ArithmeticError("Born-sampled branch unexpectedly empty")
    packet = translate_combine(packets, weights, outcomes)
    return state, packet, outcomes, probability


def copy_budget(width, normal_dimension):
    """Conservative D=3 schedule using the translation-moment rank bounds."""
    if width < 1 or normal_dimension < 1:
        raise ValueError("positive dimensions required")
    cubic = normal_dimension + 1
    quadratic = (normal_dimension * (width + 1) + 1) ** 2
    linear = normal_dimension * comb(width + 2, 2) + 1
    return {"3": cubic, "2": quadratic, "1": linear,
            "original_cosets_per_output": cubic * quadratic * linear}
