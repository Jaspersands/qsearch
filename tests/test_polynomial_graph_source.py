"""Exact F25/UT3 source falsifiers, not a solver or a hard-instance claim."""

from collections import Counter
from fractions import Fraction
from itertools import product

from flint import fmpz_mod_poly_ctx, fq_default_ctx
import pytest
import sympy as sp

from theorems.ut5_matrix_phase_alignment import _lists, _matrix, _product


P = 5
Q = 25
VARIABLES = sp.symbols("x y z")


def _ut3(a, b, c):
    return ((1, a, c), (0, 1, b), (0, 0, 1))


def _formal_difference(inverse_row, exponent):
    x = VARIABLES[0]
    image = sum(a*v for a, v in zip(inverse_row, VARIABLES))
    return sp.Poly(image**exponent-image-(x**exponent-x),
                   *VARIABLES, modulus=P)


@pytest.fixture(scope="module")
def field25():
    field = fq_default_ctx(modulus=fmpz_mod_poly_ctx(P)([2, 4, 1]))
    assert field.modulus().is_irreducible()
    theta = field.gen()
    elements = tuple(field(a)+b*theta for a, b in product(range(P), repeat=2))
    assert len(set(elements)) == Q
    for value in elements:
        assert field(int(value.trace())) == value+value**P
    return field, elements


@pytest.fixture(scope="module")
def formal_orbit():
    group = tuple(_ut3(*abc) for abc in product(range(P), repeat=3))
    rows = {g: tuple(_lists(_matrix(g, P).inv())[0]) for g in group}
    differences = {g: _formal_difference(rows[g], P) for g in group}
    assert len(group) == 125
    assert len(set(rows.values())) == 25
    return group, rows, differences


@pytest.fixture(scope="module")
def graph_differences(field25, formal_orbit):
    field, elements = field25
    group, rows, _ = formal_orbit
    values = {x: x**P-x for x in elements}
    histograms = {}
    # Only 25 distinct inverse first rows; evaluate each on the 25^3 points.
    for row in set(rows.values()):
        assert row[0] == 1
        counts = Counter()
        for y, z in product(elements, repeat=2):
            shift = row[1]*y+row[2]*z
            for x in elements:
                counts[values[x+shift]-values[x]] += 1
        assert sum(counts.values()) == Q**3
        assert counts[field(0)] > 0
        histograms[row] = counts
    return {g: histograms[rows[g]] for g in group}


def test_formal_stabilizer_is_the_proper_nonnormal_ut3_subgroup(formal_orbit):
    group, _, differences = formal_orbit
    stabilizer = {g for g in group if differences[g].is_zero}
    assert stabilizer == {_ut3(0, b, 0) for b in range(P)}
    assert len(stabilizer) == 5 < len(group)
    for g, h in product(stabilizer, repeat=2):
        assert tuple(map(tuple, _product(g, h, P))) in stabilizer

    g, h = _ut3(1, 0, 0), _ut3(0, 1, 0)
    conjugate = _matrix(g, P)*_matrix(h, P)*_matrix(g, P).inv()
    conjugate = tuple(map(tuple, _lists(conjugate)))
    assert conjugate == _ut3(0, 1, 1)
    assert h in stabilizer and conjugate in group
    assert conjugate not in stabilizer
    assert not differences[conjugate].is_zero


def test_single_trace_phase_loses_formal_symmetry_over_f25(
        field25, formal_orbit, graph_differences):
    field, elements = field25
    group, _, differences = formal_orbit
    values = tuple(x**P-x for x in elements)
    assert any(value != field(0) for value in values)
    assert Counter(int(value.trace()) for value in values) == Counter({0: Q})

    for g in group:
        traces = Counter()
        for difference, multiplicity in graph_differences[g].items():
            traces[int(difference.trace())] += multiplicity
        # Every phase difference is exactly 1, including all 120 non-symmetries.
        assert traces == Counter({0: Q**3})
    assert sum(not differences[g].is_zero for g in group) == 120


def test_full_character_tag_restores_exact_graph_overlap(
        field25, formal_orbit, graph_differences):
    field, elements = field25
    group, _, differences = formal_orbit
    characters = {}
    for difference in elements:
        counts = Counter(int((u*difference).trace()) for u in elements)
        expected = ({0: Q} if difference == field(0)
                    else {r: Q//P for r in range(P)})
        assert counts == Counter(expected)
        characters[difference] = counts

    for g in group:
        counts = graph_differences[g]
        tagged = Counter()
        for difference, multiplicity in counts.items():
            for phase, frequency in characters[difference].items():
                tagged[phase] += multiplicity*frequency
        assert sum(tagged.values()) == Q**4
        # Subtract a multiple of 1+w+w^2+w^3+w^4=0, without floating phases.
        assert all(tagged[r] == tagged[P-1] for r in range(1, P))
        tagged_overlap = Fraction(tagged[0]-tagged[P-1], Q**4)
        graph_overlap = Fraction(counts[field(0)], Q**3)
        expected = Fraction(1) if differences[g].is_zero else Fraction(1, 5)
        assert tagged_overlap == graph_overlap == expected


def test_wrong_field_aliases_nonzero_formal_polynomial_to_zero(field25):
    field, elements = field25
    x = VARIABLES[0]
    polynomial = sp.Poly(x**Q-x, *VARIABLES, modulus=P)
    assert not polynomial.is_zero
    assert polynomial.total_degree() == Q
    inverse_row = tuple(_lists(_matrix(_ut3(1, 0, 0), P).inv())[0])
    assert not _formal_difference(inverse_row, Q).is_zero

    assert Counter(value**Q-value for value in elements) == Counter({field(0): Q})
    # Thus its evaluation graph is uniform |x>|0> on F25^3 despite that shear.
