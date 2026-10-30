"""Exact GIJS Hasse-operator field-lift counterexample, without producer imports.

This guards a binary-versus-complex translation, not a Goppa-instance claim or
a general quantum lower bound. Jets are extracted from polynomial expansions.
"""

from itertools import combinations

import pytest
import sympy as sp


_K = 6
_DEGREE = 3
_ORDER = 2
_MONOMIALS = tuple(combinations(range(_K), _DEGREE))
_ZERO = (0,) * _K
_UNITS = tuple(tuple(int(i == j) for i in range(_K)) for j in range(_K))
_DERIVATIVES = (_ZERO,) + _UNITS
_A = (0, 0, 1, 1, 1, 0)
_C = (1, 1, 0, 0, 1, 0)
_HELD_OUT = (1, 1, 1, 1, 0, 0)


def _expand_translated_monomial(monomial, point):
    """Multiply the factors (point[i] + Z_i) over the integers."""
    polynomial = {_ZERO: 1}
    for variable in monomial:
        expanded = {}
        for powers, coefficient in polynomial.items():
            constant = coefficient * point[variable]
            if constant:
                expanded[powers] = expanded.get(powers, 0) + constant
            shifted = list(powers)
            shifted[variable] += 1
            shifted = tuple(shifted)
            expanded[shifted] = expanded.get(shifted, 0) + coefficient
        polynomial = expanded
    return polynomial


def _jet_matrix(points):
    rows = []
    for monomial in _MONOMIALS:
        row = []
        for point in points:
            expansion = _expand_translated_monomial(monomial, point)
            row.extend(expansion.get(powers, 0) for powers in _DERIVATIVES)
        rows.append(row)
    return sp.ImmutableMatrix(rows)


def _vector(*monomials):
    """Coefficient vector for the specified one-based square-free monomials."""
    support = {tuple(i - 1 for i in monomial) for monomial in monomials}
    return sp.ImmutableMatrix([int(monomial in support) for monomial in _MONOMIALS])


def _gf2_rank(matrix):
    # Dense row elimination, independent of producer and SymPy rank routines.
    rows = [[int(value) % 2 for value in row] for row in matrix.tolist()]
    rank = 0
    for column in range(matrix.cols):
        pivot = next(
            (row for row in range(rank, matrix.rows) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for row in range(rank + 1, matrix.rows):
            if rows[row][column]:
                rows[row] = [x ^ y for x, y in zip(rows[row], rows[rank])]
        rank += 1
        if rank == matrix.rows:
            break
    return rank


@pytest.fixture(scope="module")
def jet_model():
    full = _jet_matrix(_UNITS + (_A, _C))
    reduced = _jet_matrix((_A, _C))
    held_out = sp.ImmutableMatrix(
        [
            _expand_translated_monomial(monomial, _HELD_OUT).get(_ZERO, 0)
            for monomial in _MONOMIALS
        ]
    )
    return full, reduced, held_out


def test_jets_are_coefficients_of_translated_polynomial_products():
    assert _expand_translated_monomial((0, 2, 4), _A) == {
        (1, 0, 0, 0, 0, 0): 1,
        (1, 0, 1, 0, 0, 0): 1,
        (1, 0, 0, 0, 1, 0): 1,
        (1, 0, 1, 0, 1, 0): 1,
    }


def test_full_systematic_columns_are_zero(jet_model):
    full, reduced, _ = jet_model
    assert _DEGREE > _ORDER >= 2
    assert full.shape == (20, 56)
    assert reduced.shape == (20, 14)
    assert full[:, :42] == sp.zeros(20, 42)
    assert full[:, 42:] == reduced
    assert reduced.cols < reduced.rows
    assert set(full) == {0, 1}


def test_expanded_jet_columns_and_held_out_vector(jet_model):
    _, reduced, held_out = jet_model
    e345 = _vector((3, 4, 5))
    e125 = _vector((1, 2, 5))
    expected = sp.Matrix.hstack(
        e345,
        _vector((1, 3, 4), (1, 3, 5), (1, 4, 5)),
        _vector((2, 3, 4), (2, 3, 5), (2, 4, 5)),
        e345,
        e345,
        e345,
        _vector((3, 4, 6), (3, 5, 6), (4, 5, 6)),
        e125,
        e125,
        e125,
        _vector((1, 2, 3), (1, 3, 5), (2, 3, 5)),
        _vector((1, 2, 4), (1, 4, 5), (2, 4, 5)),
        e125,
        _vector((1, 2, 6), (1, 5, 6), (2, 5, 6)),
    )
    assert reduced == expected
    assert held_out == _vector((1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4))


def test_four_column_integer_identity_certifies_binary_membership(jet_model):
    full, reduced, held_out = jet_model
    witness = sp.zeros(14, 1)
    for column in (1, 2, 10, 11):
        witness[column] = 1
    doubled = _vector((1, 3, 5), (1, 4, 5), (2, 3, 5), (2, 4, 5))
    assert reduced * witness == held_out + 2 * doubled
    assert (reduced * witness - held_out).applyfunc(lambda x: x % 2) == sp.zeros(20, 1)
    full_witness = sp.zeros(42, 1).col_join(witness)
    assert full * full_witness == reduced * witness


def test_rational_annihilator_separates_held_out_vector(jet_model):
    full, reduced, held_out = jet_model
    annihilator = _vector((1, 3, 5)) - _vector((1, 3, 4)) - _vector((1, 2, 3))
    assert annihilator.T * reduced == sp.zeros(1, 14)
    assert annihilator.T * full == sp.zeros(1, 56)
    assert (annihilator.T * held_out)[0] == -2
    binary_annihilator = annihilator.applyfunc(lambda x: x % 2)
    assert (binary_annihilator.T * reduced).applyfunc(lambda x: x % 2) == sp.zeros(1, 14)
    assert (binary_annihilator.T * held_out)[0] % 2 == 0


@pytest.mark.parametrize("matrix_index", (0, 1), ids=("full", "reduced"))
def test_binary_and_rational_membership_ranks_disagree(jet_model, matrix_index):
    matrix = jet_model[matrix_index]
    held_out = jet_model[2]
    augmented = matrix.row_join(held_out)
    assert (_gf2_rank(matrix), _gf2_rank(augmented)) == (8, 8)
    assert (matrix.rank(), augmented.rank()) == (8, 9)


def test_exact_gram_characteristic_polynomial(jet_model):
    full, reduced, _ = jet_model
    gram = reduced * reduced.T
    assert full * full.T == gram
    variable = sp.Symbol("lambda")
    expected = (
        variable**12
        * (variable - 1)
        * (variable - 3) ** 4
        * (variable - 4) ** 2
        * (variable - 5)
    )
    assert sp.Poly(gram.charpoly(variable).as_expr(), variable) == sp.Poly(expected, variable)


def test_exact_real_left_kernel_projection_has_weight_four_fifths(jet_model):
    _, reduced, held_out = jet_model
    basis = sp.Matrix.hstack(*reduced.columnspace())
    projection = basis * (basis.T * basis).inv() * basis.T * held_out
    residual = held_out - projection
    expected_projection = sp.Rational(1, 5) * (
        reduced[:, 1] + reduced[:, 2] + reduced[:, 10] + reduced[:, 11]
    )
    assert projection == expected_projection
    assert reduced.T * residual == sp.zeros(14, 1)
    assert (projection.T * residual)[0] == 0
    assert (held_out.T * held_out)[0] == 4
    assert (residual.T * residual)[0] == sp.Rational(16, 5)
    assert (residual.T * residual)[0] / (held_out.T * held_out)[0] == sp.Rational(4, 5)
    assert all(value.is_Rational for value in projection.col_join(residual))
