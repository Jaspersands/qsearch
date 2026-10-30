import random

import pytest
from sympy import Matrix, eye

from native_maps import OrderFiveModel, finite_points
from local_gate import ROOT, check_actions, column_basis, mod, orbit_control, pullback_control, split_control
import sys
sys.path.insert(0, str(ROOT/"frobenius-order-completion-2026-10-25"))
from completion import lagrangians
from kernel_output import alternating_form


@pytest.fixture(scope="module")
def native():
    model = OrderFiveModel(19)
    return model, finite_points(model)


def test_actual_curve_points_and_order_five_maps(native):
    model, points = native
    assert len(points)+1 == 19**2+1+4*19
    for point in points:
        divisor = model.from_points([point])
        assert model.gamma(divisor, 5) == divisor
        assert model.gamma(model.gamma(divisor), -1) == divisor
        x, y = point
        assert model.gamma(divisor) == model.from_points([(model.zeta*x, y)])
        assert model.frobenius(divisor) == model.from_points([(x**19, y**19)])
        assert model.frobenius(model.gamma(divisor)) == model.gamma(model.frobenius(divisor), -1)


def test_two_point_mumford_formulas_and_identity(native):
    model, points = native
    rng = random.Random(25)
    divisors = [model.from_points([])]
    while len(divisors) < 41:
        pair = rng.sample(points, 2)
        if pair[0][0] != pair[1][0]:
            divisor = model.from_points(pair)
            divisors.append(divisor)
            assert model.gamma(divisor) == model.from_points([(model.zeta*x, y) for x, y in pair])
    for divisor in divisors:
        moved = divisor
        for _ in range(5):
            moved = model.gamma(moved)
        assert moved == divisor
        assert model.frobenius(model.gamma(divisor)) == model.gamma(model.frobenius(divisor), -1)


@pytest.mark.parametrize("p", [19, 29, 59, 79, 109, 139, 4294967279])
def test_public_map_acquisition_does_not_enumerate_the_field(p):
    model = OrderFiveModel(p, 2)
    result = model.certificate(11)
    assert result["cartier_matrix_zero_by_support"]
    assert result["squared_rosati_norm_bounds"] == [4, 4*p]
    assert not result["incoming_isogeny_constructed"]
    assert not result["native_kernel_recovered"]
    assert model.zeta**p == model.zeta**4


def test_all_1464_lagrangians_for_the_split_spectrum():
    g, t = split_control()
    planes = tuple(lagrangians(11, cap=2000))
    assert len(planes) == (11+1)*(11**2+1) == 1464
    for plane in planes:
        assert orbit_control(plane, g, t, 19, 11)[-1] == 4


def test_automorphism_alone_is_not_the_two_map_theorem():
    g, t = split_control()
    plane = eye(4)[:, [0, 2]]
    assert column_basis(plane.row_join(g*plane), 11).cols == 2
    assert orbit_control(plane, g, t, 19, 11)[-1] == 4


def test_prime_square_source_pullbacks_match_the_orbit_prediction():
    g, t = split_control()
    for index, plane in enumerate(lagrangians(11, cap=2000)):
        if index % 97 == 0:
            ranks = pullback_control(plane, g, t, 19, 11)
            assert ranks == tuple(r-2 for r in orbit_control(plane, g, t, 19, 11)[1:])


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_chart_changes_preserve_the_algebra_and_gate(seed):
    g, t = split_control()
    rng, frame = random.Random(seed), eye(4)
    form = alternating_form(2)
    for _ in range(4):
        v = Matrix([rng.randrange(11) for _ in range(4)])
        frame *= eye(4)+v*v.T*form
    inverse = frame.inv_mod(11)
    changed_g, changed_t = mod(inverse*g*frame, 11), mod(inverse*t*frame, 11)
    plane = mod(inverse*eye(4)[:, [0, 2]], 11)
    assert orbit_control(plane, changed_g, changed_t, 19, 11) == (2, 4, 4)


def test_common_field_scalar_frobenius_is_not_substituted():
    g, _ = split_control(p=59)
    with pytest.raises(ValueError, match="inversion"):
        check_actions(g, 2*eye(4), 59, 11)


@pytest.mark.parametrize("ell", [2, 5, 19, 25])
def test_excluded_isogeny_primes(native, ell):
    with pytest.raises(ValueError):
        native[0].certificate(ell)


@pytest.mark.parametrize("p,c", [(2, 1), (5, 1), (11, 1), (24, 1), (19, 0)])
def test_unavailable_curve_contract_is_rejected(p, c):
    with pytest.raises(ValueError):
        OrderFiveModel(p, c)


def test_incorrect_divisor_and_control_budget_fail(native):
    model, _ = native
    with pytest.raises(ValueError, match="Mumford"):
        model.gamma((model.polys([0, 1]), model.polys([0])))
    with pytest.raises(ValueError, match="cap"):
        finite_points(model, cap=100)


def test_wrong_characteristic_polynomial_and_degenerate_action_rejected():
    g, t = split_control()
    with pytest.raises(ValueError, match="characteristic"):
        check_actions(eye(4), t, 19, 11)
    with pytest.raises(ValueError, match="multipliers"):
        check_actions(g, 0*t, 19, 11)
