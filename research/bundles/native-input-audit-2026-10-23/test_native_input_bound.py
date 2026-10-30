from fractions import Fraction
from itertools import product

import pytest

from native_input_bound import (ceil_log2_ratio, lagrangian_count,
                                random_mark_probability_bound, small_prime_levels,
                                sp4_order)


def test_independent_counts_in_dimension_four_over_three():
    vectors = tuple(product(range(3), repeat=4))
    nonzero = [v for v in vectors if any(v)]

    def pairing(v, w):
        return (v[0]*w[1]-v[1]*w[0]+v[2]*w[3]-v[3]*w[2]) % 3

    pairs = sum(pairing(v, w) == 1 for v in nonzero for w in vectors)
    complement = [v for v in vectors if v[0] == v[1] == 0]
    completions = sum(pairing(v, w) == 1 for v in complement for w in complement)
    assert pairs*completions == sp4_order(3) == 51840
    planes = set()
    for v in nonzero:
        multiples = {tuple(a*x % 3 for x in v) for a in range(3)}
        for w in nonzero:
            if w not in multiples and pairing(v, w) == 0:
                planes.add(frozenset(tuple((a*x+b*y) % 3 for x, y in zip(v, w))
                                    for a, b in product(range(3), repeat=2)))
    assert len(planes) == lagrangian_count(3) == 40


@pytest.mark.parametrize("a,b,expected", [(1, 1, 0), (1, 2, -1), (1, 3, -1),
                                         (1, 4, -2), (3, 2, 1), (9, 2, 3),
                                         (1, 2**1000, -1000)])
def test_exact_log_bound(a, b, expected):
    result = ceil_log2_ratio(a, b)
    assert result == expected
    assert Fraction(2)**(result-1) < Fraction(a, b) <= Fraction(2)**result


@pytest.mark.parametrize("ell", [3, 101, 65537, 2**61-1, 2**127-1])
def test_small_level_plan_and_probability_bound(ell):
    levels = small_prime_levels(ell, 37)
    result = random_mark_probability_bound(ell, 37, levels)
    assert result["level_product"] > 8*ell
    assert result["global_maps_mod_sign_upper_bound"] == 25920*(ell+1)*(ell*ell+1)
    assert result["single_trial_probability_at_most_power_of_two"] < 0
    assert result["arbitrary_algorithm_hardness_established"] is False
    assert result["global_isogeny_consistency_test_executed"] is False


def test_adding_an_independent_level_strengthens_bound():
    old = random_mark_probability_bound(101, 37, (3, 5, 7))
    new = random_mark_probability_bound(101, 37, (3, 5, 7, 11))
    def value(row):
        return Fraction(**row["single_trial_probability_upper_bound"])
    assert value(new) == value(old)/(sp4_order(11)//2)


def test_union_bound_is_capped_and_does_not_claim_hardness():
    one = random_mark_probability_bound(101, 37, (3, 5, 7))
    result = random_mark_probability_bound(101, 37, (3, 5, 7), trials=10**100)
    assert one["single_trial_probability_at_most_power_of_two"] < 0
    assert result["union_probability_upper_bound"] == {"numerator": 1, "denominator": 1}


@pytest.mark.parametrize("ell,p,levels,trials", [
    (9, 37, (5,), 1), (101, 3, (5,), 1), (37, 37, (5,), 1),
    (101, 37, (), 1), (101, 37, (3, 3), 1), (101, 37, (101,), 1),
    (101, 37, (37,), 1), (101, 37, (2,), 1), (101, 37, (3,), 0),
])
def test_invalid_models_rejected(ell, p, levels, trials):
    with pytest.raises(ValueError):
        random_mark_probability_bound(ell, p, levels, trials=trials)
