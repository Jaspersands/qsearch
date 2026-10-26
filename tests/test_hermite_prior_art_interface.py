"""Adversarial controls for the 2023 multiplicity-decoder interface.

These are algebraic counterexamples and identity checks, not quantum runs.
See research/HERMITE_DECODER_PRIOR_ART.md for source versions and scope.
"""
from fractions import Fraction
from math import comb, floor

import pytest

from theorems.folded_rs_decoder import affine_solution
from theorems.hermite_pinned_decoder import jet, operator_matrix, pin_space


def field_vanishing_polynomial(p):
    polynomial = [0] * (p + 1)
    polynomial[1], polynomial[p] = p - 1, 1
    return polynomial


def test_appendix_regular_point_premise_is_not_implied_by_its_parameters():
    p, multiplicity, degree, derivative_count = 17, 8, 63, 2
    error_fraction = Fraction(1, 4)
    radius_bound = (
        1 - Fraction(1, derivative_count + 1)
        - Fraction(derivative_count, derivative_count + 1)
        * Fraction(multiplicity, multiplicity - derivative_count + 1)
        * Fraction(degree, multiplicity * p)
    )
    interpolation_degree = floor(
        (multiplicity - derivative_count + 1) * (1 - error_fraction) * p - 1
    )
    assert error_fraction < radius_bound
    assert derivative_count <= min(multiplicity, p)
    assert interpolation_degree == 88
    assert interpolation_degree - degree >= p
    assert (interpolation_degree + 1
            + derivative_count * (interpolation_degree - degree + 1)
            > p * (multiplicity - derivative_count + 1))

    # A=B_0=0, B_1=X^p-X satisfies every interpolation constraint when
    # the received jets are zero. No base-field point has B_1(a) != 0.
    top_coefficient = field_vanishing_polynomial(p)
    assert any(top_coefficient)
    assert all(jet(top_coefficient, a, 1, p) == [0] for a in range(p))
    rows, certificate = operator_matrix(p, degree + 1, [[0], top_coefficient])
    kernel = affine_solution(p, rows, [0] * len(rows), degree + 1)
    assert certificate["unpivoted_degree_indices"] == [0, 17, 34, 51]
    assert len(kernel["basis"]) == 4


@pytest.mark.parametrize("p,order", [(3, 1), (5, 1), (5, 2), (7, 4), (17, 1)])
def test_high_degree_multiplier_preserves_coefficient_kernel_not_value_kernel(p, order):
    k = 3 * p + 2
    multiplier = field_vanishing_polynomial(p)
    coefficients = [[0] for _ in range(order)] + [multiplier]
    rows, certificate = operator_matrix(p, k, coefficients)
    kernel = affine_solution(p, rows, [0] * len(rows), k)
    free = [t for t in range(k) if comb(t, order) % p == 0]
    assert certificate["leading_degree_shift"] == p - order
    assert certificate["unpivoted_degree_indices"] == free
    assert len(kernel["basis"]) == len(free)
    assert len(free) <= order * ((k + p - 1) // p)

    # D^[order](X^order)=1. The polynomial residual is nonzero even
    # though evaluating it at every base-field point gives zero.
    residual = [row[order] for row in rows]
    assert any(residual)
    assert all(jet(residual, a, 1, p) == [0] for a in range(p))
    assert residual[:p + 1] == multiplier


def test_singleton_incomplete_list_does_not_certify_pinned_guard_uniqueness():
    p, multiplicity, k = 5, 2, 4
    zero = [0] * k
    alternative = [1, p - 2, 1, 0]  # (X-1)^2
    codewords = [
        [jet(f, a, multiplicity, p) for a in range(1, p)]
        for f in (zero, alternative)
    ]
    received = [codewords[1][i] if i in (1, 2) else codewords[0][i]
                for i in range(p - 1)]
    distances = [sum(x != y for x, y in zip(c, received)) for c in codewords]
    assert distances == [2, 1]
    assert len([zero]) == 1
    assert zero != alternative
    assert codewords[0][0] == codewords[1][0] == [0, 0]

    superspace = {"offset": zero, "basis": [alternative]}
    ambiguous = pin_space(p, multiplicity, superspace, {0: [0, 0]})
    assert len(ambiguous["basis"]) == 1
    resolved = pin_space(p, multiplicity, superspace, {0: [0, 0], 1: [0, 0]})
    assert resolved["offset"] == zero
    assert resolved["basis"] == []


def test_whole_field_padding_charges_one_extra_error():
    p, multiplicity, h = 7, 2, 1
    n = p - 1
    k = multiplicity * n // 2
    polynomial = [1] + [0] * (k - 1)
    true_jets = [jet(polynomial, a, multiplicity, p) for a in range(p)]
    received = [list(values) for values in true_jets[1:]]
    received[0][0] = 2
    padded = [[0] * multiplicity] + received
    assert sum(x != y for x, y in zip(true_jets[1:], received)) == h
    assert sum(x != y for x, y in zip(true_jets, padded)) == h + 1
    delta = 1 - Fraction(k - 1, multiplicity * p)
    gap = delta - Fraction(h + 1, p)
    assert gap == Fraction(1, 2) - Fraction(2 * h + 1, 2 * p) + Fraction(1, multiplicity * p)
    assert gap < delta - Fraction(h, p)
