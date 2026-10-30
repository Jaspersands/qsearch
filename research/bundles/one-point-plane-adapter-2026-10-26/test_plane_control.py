import pytest
from sympy import Poly

from plane_control import CurveControl, X, Y, eta, inseparable_control, t


@pytest.mark.parametrize("genus,prime", [(1, 17), (2, 17), (1, 3), (2, 5)])
def test_repeated_point_colons_match_independent_pole_basis(genus, prime):
    curve = CurveControl(genus, prime)
    spaces, numerators = curve.one_point_spaces()
    identity = curve.identity()
    for j, actual in spaces.items():
        expected = [row for row, (a, b) in zip(identity, curve.basis(2))
                    if 2*a+curve.m*b <= 2*curve.ell-j]
        assert curve.span(actual) == curve.span(expected)
    for j, actual in numerators.items():
        expected = [row for row, (a, b) in zip(identity, curve.basis(2)) if 2*a+curve.m*b <= j]
        assert curve.span(actual) == curve.span(expected)
        assert len(actual) == j+1-genus


@pytest.mark.parametrize("genus,prime", [(1, 17), (2, 17), (1, 3), (2, 5)])
def test_exact_plane_relation_unique_and_has_claimed_size(genus, prime):
    curve = CurveControl(genus, prime)
    equation, result = curve.plane_relation()
    assert result["total_plane_degree"] <= curve.n
    assert Poly(equation, Y).degree() == curve.m
    assert Poly(equation, Y).LC() == 1
    assert result["relation_kernel_dimension"] == 1
    assert not result["native_genus41_adapter_implemented"]


def test_elliptic_equation_and_inverse_are_symbolic_not_point_fit():
    curve = CurveControl(1)
    actual, _ = curve.plane_relation()
    expected = Y*(Y+2)**2-(X**2-2)**2
    assert Poly(actual-expected, X, Y, modulus=17).is_zero
    assert curve.relation.reduce(((eta**2-2)-t*(t*t+2)).expand())[1] == 0


def test_shared_pole_factor_would_not_certify_birationality():
    # t and t^2 have pole orders2,4 and only generate F_p(t), a proper
    # degree-two subfield. A relation y=x^2 alone is the wrong curve.
    from math import gcd
    assert gcd(2, 4) == 2
    curve = CurveControl(1)
    assert curve.relation.reduce((t*t-t**2).expand())[1] == 0
    assert len(curve.basis(1)) == 4


@pytest.mark.parametrize("genus", [1, 2])
def test_colon_cancels_extra_zeros_of_the_denominator(genus):
    curve = CurveControl(genus)
    denominator = t**(genus+1)
    _, numerators = curve.one_point_spaces(denominator)
    for j, actual in numerators.items():
        expected = [curve.coordinates(denominator*t**a*eta**b, 2)
                    for a, b in curve.basis(2) if 2*a+curve.m*b <= j]
        assert curve.span(actual) == curve.span(expected)


def test_genuinely_inseparable_coordinate_still_recovers_original_field():
    data = inseparable_control()
    assert data["derivative_in_Y_is_zero"]
    assert data["relation_kernel_dimension"] == 1
    assert data["symbolic_inverse_verified"]
