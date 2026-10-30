from fractions import Fraction
from itertools import product

import pytest

from class_bound import bad_class_upper, preimage_fraction_bound, tower_class_certificate


def test_native_tower_dimensions_and_exact_bound():
    data = tower_class_certificate(8)
    assert (data["genus"], data["divisor_degree"], data["length"],
            data["residual_degree_K_minus_3G_plus_D"]) == (41, 83, 176, 7)
    assert data["bad_fraction_upper_under_uniform_Pic_d"] == Fraction(41*9**41, 100003**33*315**2)
    assert 0 < data["bad_fraction_upper_under_uniform_Pic_d"] < Fraction(1, 10**128)
    assert not data["divisor_class_constructed"]
    assert not data["native_matrix_constructed"]
    assert not data["registry_admission"]


def test_bound_decreases_on_all_checked_dyadic_degrees():
    values = [tower_class_certificate(e)["bad_fraction_upper_under_uniform_Pic_d"]
              for e in (8, 16, 32, 64, 128)]
    assert all(a > b > 0 for a, b in zip(values, values[1:]))


def test_cannot_drop_torsion_factor_or_infer_uniform_image():
    group = list(product(range(3), repeat=2))
    images = [tuple(3*x % 3 for x in item) for item in group]
    bad = {(0, 0)}
    actual = Fraction(sum(image in bad for image in images), len(group))
    assert actual == preimage_fraction_bound(9, 9, 1) == 1
    assert Fraction(len(bad), len(group)) < actual


def test_nontrivial_image_coset_and_empty_intersection():
    group = range(12)
    for shift in range(12):
        for bad in ({0}, {1, 4}, {0, 3, 6, 9}, set()):
            actual = Fraction(sum((shift-3*x) % 12 in bad for x in group), 12)
            assert actual <= preimage_fraction_bound(12, 3, len(bad))
    assert preimage_fraction_bound(12, 3, 0) == 0


@pytest.mark.parametrize("args", [(9, 4, 2), (5, 0, 0), (100003, 41, 41),
                                  (True, 2, 0), (100003, True, 0)])
def test_invalid_geometric_bound_inputs(args):
    with pytest.raises(ValueError):
        bad_class_upper(*args)


def test_negative_degree_and_vacuous_bound_remain_scoped():
    assert bad_class_upper(100003, 41, -1) == 0
    assert bad_class_upper(5, 20, 19) == 1
    data = tower_class_certificate(16)
    assert data["rules_out_only_the_same_code_cubic_annihilator_method"]
    assert not data["classical_hardness_proved"]


@pytest.mark.parametrize("e", [0, 4, 9, True])
def test_non_tower_degree_rejected(e):
    with pytest.raises(ValueError):
        tower_class_certificate(e)
