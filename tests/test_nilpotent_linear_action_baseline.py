"""Finite falsifiers for the linear-action scope audit, not a solver backend."""

from itertools import product
from math import gcd, prod

import pytest
from sympy import primerange


def _gl_order(dimension, q):
    return q ** (dimension * (dimension - 1) // 2) * prod(
        q**i - 1 for i in range(1, dimension + 1)
    )


def _valuation(value, prime):
    answer = 0
    while value % prime == 0:
        value //= prime
        answer += 1
    return answer


def _split(dimension, q, characteristic):
    """Arithmetic only: no group nilpotence or field validation is implied."""
    order = _gl_order(dimension, q)
    large = order
    for prime in {*primerange(2, dimension + 1), characteristic}:
        while large % prime == 0:
            large //= prime
    small = order // large
    e_small = 0 if small == 1 else large * pow(large, -1, small)
    e_large = 0 if large == 1 else small * pow(small, -1, large)
    return small, large, e_small, e_large


def _identity(dimension):
    return tuple(tuple(int(i == j) for j in range(dimension))
                 for i in range(dimension))


def _multiply(left, right, q):
    dimension = len(left)
    return tuple(tuple(sum(left[i][k] * right[k][j]
                           for k in range(dimension)) % q
                       for j in range(dimension)) for i in range(dimension))


def _power(matrix, exponent, q):
    result = _identity(len(matrix))
    while exponent:
        if exponent & 1:
            result = _multiply(result, matrix, q)
        matrix = _multiply(matrix, matrix, q)
        exponent >>= 1
    return result


def _closure(generators, q):
    identity = _identity(len(generators[0]))
    found, pending = {identity}, [identity]
    while pending:
        element = pending.pop()
        for generator in generators:
            other = _multiply(element, generator, q)
            if other not in found:
                found.add(other)
                pending.append(other)
    return found


@pytest.mark.parametrize("q,characteristic", [(2, 2), (4, 2), (8, 2),
                                             (9, 3), (11, 11), (16, 2)])
def test_large_cross_characteristic_sylow_order_matches_abelian_torus(q, characteristic):
    for dimension in range(1, 9):
        order = _gl_order(dimension, q)
        for prime in primerange(dimension + 1, 43):
            if prime == characteristic:
                continue
            e = next(i for i in range(1, prime) if pow(q, i, prime) == 1)
            blocks = dimension // e
            assert blocks < prime
            assert _valuation(order, prime) == blocks * _valuation(q**e - 1, prime)


@pytest.mark.parametrize("dimension,q,characteristic", [
    (1, 2, 2), (1, 8, 2), (2, 4, 2), (3, 5, 5), (4, 11, 11), (7, 16, 2),
])
def test_crt_projectors_including_trivial_factors(dimension, q, characteristic):
    small, large, e_small, e_large = _split(dimension, q, characteristic)
    order = _gl_order(dimension, q)
    assert small * large == order
    assert gcd(small, large) == 1
    assert (e_small - 1) % small == e_small % large == 0
    assert e_large % small == (e_large - 1) % large == 0
    assert (e_small + e_large - 1) % order == 0
    assert (e_small**2 - e_small) % order == 0
    assert (e_large**2 - e_large) % order == 0


def _nilpotent_fixture(x, y, z, a, b):
    # UT_3(F_11) times two central C_5 factors in dimension four.
    return ((a, a*x % 11, a*z % 11, 0),
            (0, a, a*y % 11, 0), (0, 0, a, 0), (0, 0, 0, b))


def test_actual_nilpotent_matrix_stabilizer_splits_with_mixed_generators():
    small, large, e_small, e_large = _split(4, 11, 11)
    generators = (_nilpotent_fixture(1, 0, 0, 3, 1),
                  _nilpotent_fixture(0, 1, 0, 1, 3))
    small_generators = tuple(_power(g, e_small, 11) for g in generators)
    large_generators = tuple(_power(g, e_large, 11) for g in generators)
    for g, b, a in zip(generators, small_generators, large_generators):
        assert _power(b, small, 11) == _identity(4)
        assert _power(a, large, 11) == _identity(4)
        assert _multiply(b, a, 11) == g
        for other in generators:
            assert _multiply(a, other, 11) == _multiply(other, a, 11)
    assert _multiply(*small_generators, 11) != _multiply(*reversed(small_generators), 11)
    small_group = _closure(small_generators, 11)
    large_group = _closure(large_generators, 11)
    assert (len(small_group), len(large_group)) == (11**3, 25)
    assert small_group & large_group == {_identity(4)}

    def fixes_vector(matrix):
        return tuple(row[2] for row in matrix) == (0, 0, 1, 0)

    scalars = [pow(3, i, 11) for i in range(5)]
    stabilizer = set()
    for x, y, z, a, b in product(range(11), range(11), range(11), scalars, scalars):
        matrix = _nilpotent_fixture(x, y, z, a, b)
        if fixes_vector(matrix):
            stabilizer.add(matrix)
    h_small = {g for g in small_group if fixes_vector(g)}
    h_large = {g for g in large_group if fixes_vector(g)}
    assert (len(stabilizer), len(h_small), len(h_large)) == (55, 11, 5)
    assert stabilizer == {_multiply(b, a, 11) for b in h_small for a in h_large}
    for h in stabilizer:
        assert _power(h, e_small, 11) in h_small
        assert _power(h, e_large, 11) in h_large


@pytest.mark.parametrize("prime,q,root", [(3, 7, 2), (5, 11, 3)])
def test_nonabelian_cross_characteristic_boundary_requires_dimension_at_least_prime(prime, q, root):
    clock = tuple(tuple(pow(root, i, q) if i == j else 0 for j in range(prime))
                  for i in range(prime))
    shift = tuple(tuple(int(i == (j + 1) % prime) for j in range(prime))
                  for i in range(prime))
    assert _multiply(clock, shift, q) != _multiply(shift, clock, q)
    assert len(_closure((clock, shift), q)) == prime**3
    _, large, _, _ = _split(prime, q, q)
    assert large % prime != 0  # This prime belongs in the bounded-mu factor.


def test_defining_characteristic_is_not_subject_to_the_dimension_obstruction():
    x = ((1, 1, 0), (0, 1, 0), (0, 0, 1))
    y = ((1, 0, 0), (0, 1, 1), (0, 0, 1))
    assert _multiply(x, y, 5) != _multiply(y, x, 5)
    assert len(_closure((x, y), 5)) == 125  # p=5 > D=3, but defining characteristic.
    small, large, _, _ = _split(3, 5, 5)
    assert small % 125 == 0 and large % 5 != 0


def test_non_nilpotent_matrix_group_breaks_generatorwise_hall_projection():
    rotation, reflection = ((3, 0), (0, 4)), ((0, 1), (1, 0))
    assert len(_closure((rotation, reflection), 11)) == 10
    _, _, e_small, e_large = _split(2, 11, 11)
    large_rotation = _power(rotation, e_large, 11)
    assert large_rotation == rotation
    assert _multiply(rotation, reflection, 11) != _multiply(reflection, rotation, 11)
    projected_product = _power(_multiply(rotation, reflection, 11), e_small, 11)
    product_of_projections = _multiply(_power(rotation, e_small, 11),
                                       _power(reflection, e_small, 11), 11)
    assert projected_product != product_of_projections


def test_coprime_hypothesis_and_subgroup_not_transporter_are_essential():
    diagonal = {(0, 0), (1, 1)}  # Subgroup of C_2 x C_2; not coprime factors.
    first = {h for h in diagonal if h[1] == 0}
    second = {h for h in diagonal if h[0] == 0}
    assert len(diagonal) != len(first) * len(second)
    # A singleton transporter in C_5 is a coset, not power-closed.
    transporter = {1}
    assert (2 * next(iter(transporter))) % 5 not in transporter


def test_redundant_abelian_parameterization_still_has_exact_coset_fibres():
    # C_35 -> C_5, with a nonfaithful scalar action, needs no group-order oracle.
    modulus = 35
    labels = [pow(3, x, 11) for x in range(modulus)]
    hidden = {x for x in range(modulus) if labels[x] == 1}
    assert hidden == set(range(0, modulus, 5))
    for x, y in product(range(modulus), repeat=2):
        assert (labels[x] == labels[y]) == ((x-y) % modulus in hidden)
