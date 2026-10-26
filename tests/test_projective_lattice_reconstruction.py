"""Exact controls for a classical attack WITH a supplied Hom lattice.

No geometric lattice construction, isogeny evaluator or quantum oracle is
provided. Small exhaustive controls check the integer proof, not hardness.
"""

from itertools import product
from fractions import Fraction

import pytest
from flint import fmpz_mat, nmod_mat

from theorems.projective_lattice_reconstruction import (
    _exact_lll_check, _ldl, _line_lattice, reconstruct_projective_vector,
)


def diagonal(entries):
    return [[entry if i == j else 0 for j in range(len(entries))]
            for i, entry in enumerate(entries)]


def marks(vector, primes):
    return [(p, tuple(((p-1)//2 or 1) * x % p for x in vector)) for p in primes]


def norm(vector, gram):
    return sum(x*gram[i][j]*y for i, x in enumerate(vector) for j, y in enumerate(vector))


@pytest.mark.parametrize("vector,weights", [((6, 5), (2, 2)),
                                         ((0, 2, -3), (3, 5, 7)),
                                         ((-7, 11, 0, 3), (1, 2, 4, 3))])
def test_recovers_only_global_sign_with_independent_prime_scalars(vector, weights):
    gram = diagonal(weights)
    result = reconstruct_projective_vector(gram, marks(vector, [3, 5, 7, 11, 13]), norm(vector, gram))
    assert result.status == "UNIQUE_PRIMITIVE_LINE"
    expected = tuple(-x for x in vector) if next(x for x in vector if x) < 0 else vector
    assert result.primitive_vector == expected
    assert result.lll_verified


def test_large_coefficients_do_not_require_field_table_enumeration():
    vector = (2**90 + 1, 2**71, -5, 7)
    primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
              59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109,
              113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179]
    gram = diagonal([1]*4)
    result = reconstruct_projective_vector(gram, marks(vector, primes), norm(vector, gram))
    assert result.status == "UNIQUE_PRIMITIVE_LINE"
    assert result.primitive_vector == vector


def test_gaussian_isogeny_coordinates_in_an_ill_conditioned_known_basis():
    # diag(6+5i, 6-5i) has multiplier 61 and Rosati squared norm 4*61.
    # This is a supplied Gaussian sublattice containing the map, not Hom discovery.
    physical = fmpz_mat([[6, 5, 0, 0, 0, 0, 6, -5]])
    change = fmpz_mat(diagonal([1]*8))
    change[0, 1] = 10**30
    change[2, 7] = -10**25
    inverse = change.inv()
    coordinates = physical * inverse
    vector = tuple(int(coordinates[0, i]) for i in range(8))
    gram_matrix = change * fmpz_mat(diagonal([2]*8)) * change.transpose()
    gram = [[int(gram_matrix[i, j]) for j in range(8)] for i in range(8)]
    assert norm(vector, gram) == 244
    result = reconstruct_projective_vector(gram, marks(vector, [3, 5, 7, 11, 13]), 244)
    assert result.status == "UNIQUE_PRIMITIVE_LINE"
    assert result.primitive_vector == vector
    recovered = fmpz_mat([result.primitive_vector]) * change
    assert recovered == physical


def test_full_rank_quaternion_coordinate_control():
    # M_2(Z[i,j]), i^2=-1, j^2=-11; an index-power-of-two suborder.
    # The chosen map is in this supplied lattice; all auxiliary primes are odd.
    vector = (6, 5, 0, 0) + (0,)*8 + (6, -5, 0, 0)
    gram = diagonal([2, 2, 22, 22]*4)
    data = marks(vector, [3, 5, 7, 13, 17, 19])
    result = reconstruct_projective_vector(gram, data, 244)
    assert result.product_level**2 > 2**15 * 244**2
    assert result.status == "UNIQUE_PRIMITIVE_LINE"
    assert result.primitive_vector == vector
    assert result.squared_norm == 244


def test_congruence_lattice_has_the_expected_index_and_every_constraint():
    vector = (2, -3, 5)
    data = marks(vector, [3, 7, 11])
    basis = _line_lattice(3, data)
    assert abs(int(basis.det())) == (3*7*11)**2
    for p, c in data:
        j = next(i for i, x in enumerate(c) if x)
        for row in range(3):
            assert all((int(basis[row, i])*c[j] - int(basis[row, j])*c[i]) % p == 0
                       for i in range(3))


def test_exact_certificate_rejects_tampered_transform_or_reduced_gram():
    gram = fmpz_mat([[100, 3], [3, 1]])
    reduced, transform = gram.lll(transform=True, rep="gram", gram="exact")
    assert _exact_lll_check(reduced, transform, gram)
    bad = fmpz_mat([[1, 0], [0, 2]])
    assert not _exact_lll_check(reduced, bad, gram)
    reduced[0, 0] += 1
    assert not _exact_lll_check(reduced, transform, gram)


def test_gram_check_is_exact_even_after_catastrophic_float_cancellation():
    size = 10**80
    gram = [[size*size + 1, size], [size, 1]]
    mu, lengths = _ldl(gram)
    assert all(isinstance(x, Fraction) for row in mu for x in row)
    assert all(isinstance(x, Fraction) for x in lengths)
    assert lengths == [Fraction(size*size + 1), Fraction(1, size*size + 1)]
    with pytest.raises(ValueError):
        _ldl([[size*size - 1, size], [size, 1]])


def test_full_right_module_annihilator_recovers_the_kernel_not_a_row_space():
    # After coefficient recovery, supplied module action gives alpha -> phi*alpha.
    # This exact split-matrix control does not compute a geometric module basis.
    p, dimension = 61, 4
    phi = nmod_mat([[6, -5, 0, 0], [5, 6, 0, 0],
                    [0, 0, 6, 5], [0, 0, -5, 6]], p)
    columns = []
    for i, j in product(range(dimension), repeat=2):
        unit = nmod_mat([[int((a, b) == (i, j)) for b in range(dimension)]
                         for a in range(dimension)], p)
        image = phi * unit
        columns.append([int(image[a, b]) for a, b in product(range(dimension), repeat=2)])
    action = nmod_mat(list(map(list, zip(*columns))), p)
    annihilator, count = action.nullspace()
    assert count == 8
    spanning = []
    for k in range(count):
        matrix = nmod_mat([[int(annihilator[a*dimension+b, k]) for b in range(dimension)]
                          for a in range(dimension)], p)
        assert phi * matrix == nmod_mat(dimension, dimension, p)
        spanning.extend([[int(matrix[a, b]) for a in range(dimension)]
                         for b in range(dimension)])
    span = nmod_mat(list(map(list, zip(*spanning))), p)
    assert span.rank() == 2
    assert phi * span == nmod_mat(dimension, len(spanning), p)
    # Swapping the composition order is not a valid way to compute ker(phi).
    wrong = nmod_mat([[0, 0, 0, 0], [0, 0, 0, 0],
                     [0, 0, 6, -5], [0, 0, 0, 0]], p)
    assert wrong * phi == nmod_mat(dimension, dimension, p)
    assert phi * wrong != nmod_mat(dimension, dimension, p)


def test_insufficient_level_is_unknown_not_a_uniqueness_claim():
    # (1,1) and (1,-1) have the same projective mark mod 2 and norm 2.
    result = reconstruct_projective_vector(diagonal([1, 1]), [(2, (1, 1))], 2)
    assert result.status == "UNKNOWN"
    assert "strict" in result.reason
    assert 2**2 == 2*2  # Strictness matters at the boundary.


def test_dividing_a_short_lattice_vector_may_destroy_its_marks():
    result = reconstruct_projective_vector(diagonal([1, 100]), [(2, (1, 1))], 101)
    assert result.status == "UNKNOWN"
    assert "lost" in result.reason
    assert result.primitive_vector == (1, 0)


def test_norm_bound_cannot_be_silently_increased():
    vector = (6, 5)
    result = reconstruct_projective_vector(diagonal([1, 1]), marks(vector, [7, 11, 13]), 60)
    assert result.status == "UNKNOWN"
    assert "exceeds" in result.reason


def test_independent_bounded_vectors_satisfy_the_exterior_norm_lower_bound():
    gram = [[2, 1], [1, 3]]
    level = 6
    vectors = [v for v in product(range(-5, 6), repeat=2) if v != (0, 0)]
    tested = 0
    for v in vectors:
        for w in vectors:
            determinant = v[0]*w[1] - v[1]*w[0]
            if determinant == 0 or determinant % level:
                continue
            dot = sum(v[i]*gram[i][j]*w[j] for i in range(2) for j in range(2))
            exterior_norm = norm(v, gram)*norm(w, gram) - dot**2
            assert exterior_norm == determinant**2 * 5
            assert exterior_norm >= level**2
            tested += 1
    assert tested > 100


@pytest.mark.parametrize("gram,data,bound", [
    ([[1, 2], [2, 1]], [(3, (1, 1))], 1),
    ([[1, 0], [1, 1]], [(3, (1, 1))], 1),
    ([[1.0]], [(3, (1,))], 1),
    ([[1]], [(9, (1,))], 1),
    ([[1]], [(3, (0,))], 1),
    ([[1]], [(3, (1,)), (3, (1,))], 1),
    ([[1]], [], 1),
    ([[1]], [(3, (1, 2))], 1),
    ([[1]], [(3, (1,))], True),
])
def test_invalid_contract_is_rejected(gram, data, bound):
    with pytest.raises(ValueError):
        reconstruct_projective_vector(gram, data, bound)
