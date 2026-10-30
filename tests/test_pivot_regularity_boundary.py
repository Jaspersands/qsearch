"""Proof controls for a declined regular-pivot backend, not a new solver."""
from fractions import Fraction
from itertools import product
from math import gcd
from random import Random

import pytest

from theorems.pivot_power_sde import pivot_power_sde
from theorems.prime_power_rees_descent import (
    lift_regular_module_witness, verify_module_witness,
)


@pytest.mark.parametrize("p,e,a,ell", [
    (3, 2, 1, 2), (5, 2, 2, 2), (7, 3, 1, 3),
    (5, 4, 1, 3), (3, 1, 1, 2),
])
def test_anchored_nonzero_pivot_moments(p, e, a, ell):
    powers = {pow(z, e, p) for z in range(1, p)}
    alphabet = sorted(powers | {0})
    candidates = [(1,) + x for x in product(alphabet, repeat=ell-1)]
    hit = Fraction(len(powers), p)**a
    mean = len(candidates)*hit
    total = squares = bad = 0
    for flat in product(range(p), repeat=a*ell):
        rows = [flat[j*ell:(j+1)*ell] for j in range(a)]
        count = sum(all(-sum(c*z for c, z in zip(row, x)) % p in powers
                        for row in rows) for x in candidates)
        total += count
        squares += count*count
        bad += 2*count < mean
    banks = p**(a*ell)
    assert Fraction(total, banks) == mean
    variance = Fraction(squares, banks)-mean**2
    assert variance == mean*(1-hit)
    assert Fraction(bad, banks) <= min(1, 4*variance/mean**2)
    d = gcd(e, p-1)
    assert Fraction(len(powers), p) == Fraction(p-1, d*p)


def test_nonzero_observed_pivots_do_not_certify_intrinsic_full_rank():
    # The intrinsic module has TWO factors, but the residue pilot spans one.
    columns = [(1, 0), (0, 0), (4, 5)]
    field = pivot_power_sde(5, 2, [(x % 5, y % 5) for x, y in columns],
                            pilot_count=2, rank_bound=2, attempt_cap=1,
                            bit_source=Random(20261030))
    assert field["status"] == "VERIFIED"
    assert field["pilot_rank"] == 1
    assert all(field["power_vector"][i] != 0 for i in field["pilot_indices"])
    assert field["power_vector"] == (1, 0, 1)
    lift = lift_regular_module_witness(columns, [1, 0, 1], prime=5,
                                      exponents=(2, 2), degree=2)
    assert lift["status"] == "SINGULAR_FIELD_WITNESS"
    assert lift["jacobian_rank"] == 1 < lift["cyclic_rank"] == 2
    assert not lift["original_module_verified"]
    assert all(5*s*s % 25 for s in range(25) if s % 5)


def test_linear_fast_path_is_not_a_regular_pivot_policy():
    field = pivot_power_sde(5, 1, [(1,), (0,), (1,)],
                            pilot_count=1, rank_bound=1, attempt_cap=1)
    assert field["reason"] == "LINEAR_DETERMINISTIC"
    assert field["weights"] == (0, 1, 0)
    assert field["regularity_not_guaranteed"]
    columns = [(1,), (5,), (1,)]
    singular = lift_regular_module_witness(columns, field["weights"],
                                           prime=5, exponents=(2,), degree=1)
    assert singular["status"] == "SINGULAR_FIELD_WITNESS"
    assert not verify_module_witness(columns, field["weights"], prime=5,
                                     exponents=(2,), degree=1)
    regular = lift_regular_module_witness(columns, [4, 1, 1],
                                          prime=5, exponents=(2,), degree=1)
    assert regular["original_module_verified"]
    assert regular["scales"] == [19, 1, 1]


def test_regular_witness_can_exist_outside_anchored_search_family():
    p = 3
    # Basis [1], suffix [1,2]. The first suffix must be active in this family.
    assert {-sum(c*x for c, x in zip([1, 2], [1, z])) % p
            for z in (0, 1)} == {0, 2}
    assert {pow(s, 2, p) for s in (1, 2)} == {1}
    witness = [1, 0, 1]
    lift = lift_regular_module_witness([(1,), (1,), (2,)], witness,
                                      prime=p, exponents=(1,), degree=2)
    assert lift["original_module_verified"]
    assert lift["jacobian_rank"] == 1


def test_nonzero_only_suffix_alphabet_collapses_at_maximal_power_index():
    p, e = 5, 4
    powers = {pow(z, e, p) for z in range(1, p)}
    assert powers == {1}
    for ell in range(1, 9):
        assert len(powers)**(ell-1) == 1
        assert len(powers | {0})**(ell-1) == 2**(ell-1)


@pytest.mark.parametrize("degree", [1, 2, 3, 4])
def test_full_rank_nonzero_pivots_lift_with_original_degree_and_frozen_zero(degree):
    columns = [(1, 5), (0, 1), (7, 11), (4, 9)]
    field = [1, 1, 0, 1]
    lift = lift_regular_module_witness(columns, field, prime=5,
                                      exponents=(2, 3), degree=degree)
    assert lift["status"] == "VERIFIED_REGULAR_MODULE_WITNESS"
    assert lift["jacobian_rank"] == lift["cyclic_rank"] == 2
    assert lift["scales"][2] == 0
    assert all(s % 5 for i, s in enumerate(lift["scales"]) if field[i])
    assert verify_module_witness(columns, lift["scales"], prime=5,
                                 exponents=(2, 3), degree=degree)


def test_characteristic_dividing_original_degree_is_not_a_lifting_promise():
    with pytest.raises(ValueError, match="degree < prime"):
        lift_regular_module_witness([(1,), (4,)], [1, 1], prime=5,
                                    exponents=(2,), degree=5)
