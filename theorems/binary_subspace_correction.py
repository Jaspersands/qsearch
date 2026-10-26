"""Exact arithmetic for the masked inverse-trace classical attack.

These utilities neither verify an MDS promise nor certify accepted subspaces.
The caller must establish those contracts; see INVERSE_TRACE_MASK_CLOSURE.md.
No quantum algorithm, oracle, or field-sized enumeration is implemented.
"""

from dataclasses import dataclass
from fractions import Fraction
from math import comb


def _integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


@dataclass(frozen=True)
class BinaryCorrection:
    rank: int
    coefficients: int | None


def solve_binary_columns(columns, target, rows):
    """Solve XOR(selected columns) = target; None means outside this span.

    Integer bit j represents row j; coefficient bit i selects column i.
    A rank-deficient matrix may still solve the supplied target. Failure is
    not evidence that the original nonlinear relation has no solution.
    """
    _integer(rows, "rows", 1)
    _integer(target, "target")
    if target >= 1 << rows:
        raise ValueError("target exceeds the declared row width")
    pivots = {}
    for index, column in enumerate(columns):
        _integer(column, "column")
        if column >= 1 << rows:
            raise ValueError("column exceeds the declared row width")
        vector, witness = column, 1 << index
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = (vector, witness)
                break
            old_vector, old_witness = pivots[pivot]
            vector ^= old_vector
            witness ^= old_witness
    coefficients = 0
    while target:
        pivot = target.bit_length() - 1
        if pivot not in pivots:
            return BinaryCorrection(len(pivots), None)
        vector, witness = pivots[pivot]
        target ^= vector
        coefficients ^= witness
    return BinaryCorrection(len(pivots), coefficients)


def random_subspace_annihilation_probability(bits, dimension):
    """Probability a uniform dimension-m subspace lies in one hyperplane."""
    _integer(bits, "bits", 1)
    _integer(dimension, "dimension", 1)
    if dimension > bits:
        raise ValueError("dimension exceeds the ambient dimension")
    return Fraction((1 << (bits - dimension)) - 1, (1 << bits) - 1)


@dataclass(frozen=True)
class MaskRankBound:
    expected_nonzero_annihilators: Fraction
    failure_upper_bound: Fraction
    simple_upper_bound: Fraction
    simultaneous_support_upper_bound: Fraction | None


def mds_mask_rank_bound(bits, checks, zero_coordinates, dimension, *, population=None):
    """Conditional bound for independent uniform binary coordinate masks.

    H over F_(2^bits) must have every checks columns independent. The zero
    support must be fixed independently of the masks, unless using the
    separately union-bounded simultaneous-support result. These are input
    promises, not properties checked by this integer calculation.
    """
    a = random_subspace_annihilation_probability(bits, dimension)
    _integer(checks, "checks", 1)
    _integer(zero_coordinates, "zero_coordinates", checks)
    if population is not None:
        _integer(population, "population", zero_coordinates)
    q, z = 1 << bits, zero_coordinates
    moment = sum(
        (comb(z, t) * (1 - a)**t * a**(z - t) * (q**(checks - t) - 1)
         for t in range(checks)),
        Fraction(0),
    )
    exponent = bits * checks - dimension * z
    simple = Fraction(1 << exponent) if exponent >= 0 else Fraction(1, 1 << -exponent)
    failure = min(Fraction(1), moment)
    simultaneous = None
    if population is not None:
        simultaneous = min(Fraction(1), comb(population, z) * moment)
    return MaskRankBound(moment, failure, min(Fraction(1), simple), simultaneous)
