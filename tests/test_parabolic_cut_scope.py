"""Countercontrols to invalid blanket exclusions, not candidate algorithms."""

from fractions import Fraction
from itertools import product

import pytest


@pytest.mark.parametrize('field_bits', [8, 32, 128])
def test_rank_one_transvection_cost_is_exponential_in_field_bits(field_bits):
    q = 2**field_bits
    dimension, codimension = 4, 1
    exact_expected_draws = sum(
        (Fraction(q**dimension - 1, q**(dimension - codimension) - q**j)
         for j in range(dimension - codimension)), Fraction(0)
    )
    assert exact_expected_draws >= q
    first = Fraction(q**dimension - 1, q**(dimension - codimension) - 1)
    assert first >= 2**(field_bits - 1)


@pytest.mark.parametrize('p', [3, 5, 7])
def test_maximal_orthogonal_reflection_sampler_has_zero_acceptance(p):
    def quadratic(v):
        return (v[0] * v[2] + v[1] * v[3]) % p

    nonsingular = [v for v in product(range(p), repeat=4) if quadratic(v)]
    accepted = [v for v in nonsingular if v[2] == v[3] == 0]
    assert nonsingular
    assert accepted == []


def test_odd_unitary_accepted_vectors_do_not_span_orthogonal_complement():
    # F4=F2[a]/(a^2+a+1), conjugation x -> x^2.
    def mul(a, b):
        value = 0
        while b:
            if b & 1:
                value ^= a
            b >>= 1
            a <<= 1
            if a & 4:
                a ^= 7
        return value

    def norm(v):
        x, y, z = v
        return mul(x, mul(y, y)) ^ mul(y, mul(x, x)) ^ mul(z, mul(z, z))

    # U=<e0>, Uperp={(x,0,z)}; its quotient by U is anisotropic.
    complement = [(x, 0, z) for x, z in product(range(4), repeat=2)]
    accepted = [v for v in complement if norm(v) == 0]
    assert len(complement) == 16
    assert accepted == [(x, 0, 0) for x in range(4)]
    assert all(v[2] == 0 for v in accepted)
