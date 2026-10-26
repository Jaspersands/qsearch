"""Exact endomorphism-lattice controls, not an implemented isogeny oracle.

Matrices describe Gaussian-integer maps on E**g with E:y^2=x^3-x over
characteristic 101. The geometric source proof is in the research note.
The tests do not construct curves, quotient models or torsion points.
"""

import itertools
from math import gcd, isqrt

import pytest
from flint import fmpz_mat, nmod_mat

from theorems.siegel_marked_source import separation_budget


def identity(n):
    return fmpz_mat([[int(r == c) for c in range(n)] for r in range(n)])


def complex_structure(g):
    return fmpz_mat([[(-1 if r < g and c == r + g else
                       1 if r >= g and c == r - g else 0)
                      for c in range(2 * g)] for r in range(2 * g)])


def gaussian(a, b, g):
    return a * identity(2 * g) + b * complex_structure(g)


def complex_matrix(entries):
    """Exact real lattice matrix of a Gaussian-integer matrix."""
    g = len(entries)
    real = [[entries[r][c][0] for c in range(g)] for r in range(g)]
    imag = [[entries[r][c][1] for c in range(g)] for r in range(g)]
    return fmpz_mat([real[r] + [-x for x in imag[r]] for r in range(g)]
                   + [imag[r] + real[r] for r in range(g)])


def kernel_key(matrix, prime):
    basis, rank = nmod_mat(matrix.tolist(), prime).nullspace()
    rows = [[int(basis[r, c]) for r in range(basis.nrows())] for c in range(rank)]
    reduced, actual = nmod_mat(rows, prime).rref()
    assert actual == rank
    return tuple(tuple(int(reduced[r, c]) for c in range(reduced.ncols())) for r in range(rank))


def key(matrix, modulus):
    return tuple(int(v) % modulus for row in matrix.tolist() for v in row)


def projective_key(matrix, modulus):
    # Only small test levels are enumerated, never the large CRT product.
    return min(key(unit * matrix, modulus) for unit in range(1, modulus) if gcd(unit, modulus) == 1)


def gaussian_units(g):
    i = complex_structure(g)
    e = identity(2 * g)
    return (e, -e, i, -i)


def joint_key(matrix, orders, g):
    return min(tuple(projective_key(unit * matrix, order) for order in orders)
               for unit in gaussian_units(g))


def independently_canonicalized_key(matrix, orders, g):
    return tuple(min(projective_key(unit * matrix, order) for unit in gaussian_units(g))
                 for order in orders)


@pytest.mark.parametrize('g', [1, 2, 3])
def test_unknown_scalar_requires_more_than_the_exact_marking_bound(g):
    plus, minus = gaussian(6, 5, g), gaussian(6, -5, g)
    unit = identity(2 * g)
    assert plus.transpose() * plus == 61 * unit
    assert minus.transpose() * minus == 61 * unit
    assert abs(int(plus.det())) == 61**g  # d is NOT the geometric degree for g>1.
    assert kernel_key(plus, 61) != kernel_key(minus, 61)
    orders = (4, 3, 5)
    assert all(projective_key(plus, r) == projective_key(minus, r) for r in orders)
    assert any(key(plus, r) != key(minus, r) for r in orders)
    exact = separation_budget(g, 61, orders, 101, 'exact')
    weak = separation_budget(g, 61, orders, 101, 'projective')
    assert exact.strict_separation
    assert not weak.strict_separation
    assert exact.level == weak.level == 60


def test_trace_free_projection_is_integral_divisible_and_within_claimed_norm():
    g, d, level = 2, 61, 60
    plus, minus = gaussian(6, 5, g), gaussian(6, -5, g)
    cross = plus.transpose() * minus
    trace = sum(int(cross[i, i]) for i in range(2 * g))
    beta = (2 * g) * cross - trace * identity(2 * g)
    assert cross.transpose() * cross == d * d * identity(2 * g)
    assert all(int(v) % level == 0 for row in beta.tolist() for v in row)
    norm = sum(int(v)**2 for row in beta.tolist() for v in row)
    assert norm == 230400
    assert 0 < norm <= 8 * g**3 * d**2
    assert norm // (level * level) == 64  # Nonzero integral remainder survives.


def test_separate_codomain_isomorphisms_per_level_break_the_stronger_bound():
    g = 2
    plus, minus = gaussian(6, 5, g), gaussian(6, -5, g)
    orders = (4, 3, 5, 11)
    certificate = separation_budget(g, 61, orders, 101, 'projective')
    assert certificate.level == 660
    assert certificate.strict_separation
    assert independently_canonicalized_key(plus, orders, g) == independently_canonicalized_key(minus, orders, g)
    assert joint_key(plus, orders, g) != joint_key(minus, orders, g)
    assert kernel_key(plus, 61) != kernel_key(minus, 61)
    # At level 3 the common isomorphism must have real phase; at 11 it must
    # have imaginary phase. These incompatible choices cannot be combined.
    options = [{u for u, unit in enumerate(gaussian_units(g))
                if projective_key(unit * plus, r) == projective_key(minus, r)} for r in orders]
    assert all(options)
    assert not set.intersection(*options)


def test_a_different_scalar_per_point_is_not_a_common_weak_scalar():
    left, right = identity(2), fmpz_mat([[1, 0], [0, 2]])
    p = 5
    assert projective_key(left, p) != projective_key(right, p)
    for c in range(2):
        x = fmpz_mat([[int(left[r, c])] for r in range(2)])
        y = fmpz_mat([[int(right[r, c])] for r in range(2)])
        assert projective_key(x, p) == projective_key(y, p)


def test_a_numeric_separation_budget_does_not_validate_weak_scalar_units():
    orders = (4, 3, 5, 11)
    assert separation_budget(2, 61, orders, 101, 'projective').strict_separation
    plus, minus = gaussian(6, 5, 2), gaussian(6, -5, 2)
    assert kernel_key(plus, 61) != kernel_key(minus, 61)
    # An evaluator multiplying by r at order r destroys all information.
    # The bound checker has no geometric/point input and cannot detect this.
    assert all(projective_key(r * plus, r) == projective_key(r * minus, r) for r in orders)


@pytest.mark.parametrize('orders', [(4, 3, 5, 11), (7, 11, 13)])
def test_dropping_polarization_defeats_arbitrarily_large_exact_marks(orders):
    certificate = separation_budget(2, 61, orders, 101, 'projective')
    assert certificate.strict_separation
    m = certificate.level
    phi = complex_matrix([[(6, 5), (0, 0)], [(0, 0), (6, -5)]])
    psi = phi.transpose()
    inverse_d = pow(61, -1, m)
    z = (11 * inverse_d % m, -60 * inverse_d % m)
    w = (11 * inverse_d % m, 60 * inverse_d % m)
    upper = complex_matrix([[(1, 0), z], [(0, 0), (1, 0)]])
    lower = complex_matrix([[(1, 0), (0, 0)], [(-w[0], -w[1]), (1, 0)]])
    rotation = complex_matrix([[(0, 0), (-1, 0)], [(1, 0), (0, 0)]])
    # A product of elementary Gaussian matrices is a genuine degree-one
    # automorphism of E**2; the modular representatives need not be units.
    u = upper * lower * upper * rotation
    assert u.det() == 1
    assert phi.transpose() * phi == 61 * identity(4)
    assert psi.transpose() * psi == 61 * identity(4)
    assert kernel_key(phi, 61) != kernel_key(psi, 61)
    assert all(int(v) % m == 0 for row in (u * phi - psi).tolist() for v in row)
    assert u.transpose() * u != identity(4)  # The forbidden missing hypothesis.


@pytest.mark.parametrize('d', [5, 13, 29, 61])
def test_joint_strong_marks_distinguish_small_gaussian_kernel_classes(d):
    g = 2
    orders = tuple(r for r in (3, 5, 7, 11, 13) if d % r)
    assert separation_budget(g, d, orders, 101, 'projective').strict_separation
    maps = [gaussian(a, b, g) for a, b in itertools.product(range(-isqrt(d), isqrt(d) + 1), repeat=2)
            if a*a + b*b == d]
    assert len(maps) == 8
    classes = {}
    for matrix in maps:
        label = joint_key(matrix, orders, g)
        hidden = kernel_key(matrix, d)
        if label in classes:
            assert classes[label] == hidden
        classes[label] = hidden
    assert len(classes) == 2
    # Multiplying by a single polarized Gaussian automorphism preserves
    # the JOINT label, not just each local label independently.
    for matrix in maps:
        assert joint_key(complex_structure(g) * matrix, orders, g) == joint_key(matrix, orders, g)


def test_weak_bound_uses_exact_integer_arithmetic_at_large_degree():
    d = 2**127 - 1
    result = separation_budget(2, d, (4, 3, 5, 11), 101, 'projective')
    assert result.rosati_square_bound == 64 * d*d
    assert result.minimum_sufficient_level == 8 * d + 1
    assert not result.strict_separation
    assert result.marked_basis_points == 16


@pytest.mark.parametrize('orders', [(4, 2), (3, 3), (61,), (101,), (), (1,)])
def test_non_coprime_or_missing_levels_do_not_receive_a_certificate(orders):
    with pytest.raises(ValueError):
        separation_budget(2, 61, orders, 101, 'projective')


@pytest.mark.parametrize('g,d,characteristic,mode', [(0, 61, 101, 'exact'),
    (2, 0, 101, 'exact'), (2, 61, 1, 'exact'), (2, 61, 101, 'opaque'),
    (2.5, 61, 101, 'exact'), (True, 61, 101, 'exact')])
def test_invalid_bound_inputs_are_rejected(g, d, characteristic, mode):
    with pytest.raises(ValueError):
        separation_budget(g, d, (3, 5), characteristic, mode)
