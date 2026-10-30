from fractions import Fraction
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_controls import local_split_bit, prime_class_bound, seed_kernel


@pytest.mark.parametrize("e", [8, 16, 32, 64])
def test_prime_class_bound_is_small_but_not_uniform_class_claim(e):
    result = prime_class_bound(e)
    assert result["bad_prime_probability_upper"] < Fraction(1, 10**126)
    assert result["corrected_prime_sampler_success_lower"] >= Fraction(
        1, 8*result["prime_divisor_degree"])
    assert result["maximum_class_mass_inflation_upper"] > 1
    assert result["native_curve_or_prime_generated"] is False
    assert result["uniform_Picard_class_distribution_claimed"] is False


def test_prime_class_ratio_and_prime_count_base_certificates():
    q, g, d = 100003, 41, 83
    assert q**d >= 4*(g+1)**2*(d+6)**2
    assert Fraction(318**2, q)**5 < 2
    assert Fraction(8*9**5, q**3) < 1
    assert prime_class_bound(16)["bad_prime_probability_upper"] < prime_class_bound(8)["bad_prime_probability_upper"]


def test_exact_large_fraction_receipt_roundtrip_without_decimal_digit_limit():
    from verify_source import jsonable
    value = prime_class_bound(64)["bad_prime_probability_upper"]
    encoded = jsonable(value)
    assert Fraction(int(encoded["numerator_hex"], 16),
                    int(encoded["denominator_hex"], 16)) == value


def test_actual_seed_split_kernel_and_constant_extension_exclusion():
    data = seed_kernel()
    assert data["marked_places"] == 23
    assert data["matrix_rank"] == 1
    assert data["kernel_dimension"] == 12
    assert all(vector[0] == 0 for vector in data["kernel_basis"])
    assert data["higher_tower_level_generated"] is False


@pytest.mark.parametrize("p", [3, 5, 7, 13])
def test_regularized_unit_invariant_under_square_and_uniformizer_changes(p):
    for valuation in (-8, -2, 0, 2, 10):
        for unit in range(1, p):
            bit = local_split_bit(p, valuation, unit)
            for scale in range(1, p):
                transformed = unit*pow(scale, -valuation, p) % p
                assert local_split_bit(p, valuation, transformed) == bit
                assert local_split_bit(p, valuation, unit*scale**2 % p) == bit


def test_zero_raw_evaluation_and_ramification_are_not_split_certificates():
    with pytest.raises(ValueError):
        local_split_bit(5, 2, 0)
    with pytest.raises(ValueError):
        local_split_bit(5, 1, 1)
    assert local_split_bit(5, 2, 2) == 1
    assert local_split_bit(5, -2, 4) == 0


@pytest.mark.parametrize("e", [0, 4, 9, True])
def test_bad_tower_parameters(e):
    with pytest.raises(ValueError):
        prime_class_bound(e)
