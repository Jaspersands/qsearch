from pathlib import Path
import sys

import pytest
from sympy import Matrix, Rational, eye, zeros

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "smooth-repolarization-2026-10-23"))
from polarization_probe import (
    completion_control, gram_matrix, low_degree_witness, neighbor_fixture,
    noncommuting_corners, norm, norm_table, unit_projectors,
    matrix_multiply,
)
from smooth_repolarization import certificate, verify_certificate


@pytest.fixture(scope="module")
def fixture():
    order, alpha, _ = neighbor_fixture(47, twisted=True)
    table, resources = norm_table(order, 8)
    return order, alpha, table, resources


@pytest.mark.parametrize("p,twisted", [(23, False), (47, True), (59, True)])
def test_order_discriminant_orientation_and_units(p, twisted):
    order, alpha, _ = neighbor_fixture(p, twisted=twisted)
    gram = Matrix(4, 4, lambda i, j:
                  (order.traces*order.multiply(order.star(eye(4)[:, i]), eye(4)[:, j]))[0])
    assert abs(gram.det()) == p*p
    assert order.multiply(alpha, alpha) == (
        -p*order.unit if twisted else alpha-((p+1)//4)*order.unit)
    table, _ = norm_table(order, 1)
    assert len(table[1]) == 2


def test_invalid_orientation_rejected():
    with pytest.raises(ValueError, match="quadratic orientation"):
        neighbor_fixture(23, direction=(1, 0))


def test_extra_automorphism_control_not_promoted():
    with pytest.raises(ValueError, match="extra-automorphism"):
        completion_control(characteristic=23, twisted=True)


@pytest.mark.parametrize("bound,budget", [(-1, 100), (True, 100), (1, 0), (8, 1)])
def test_enumeration_preflight(fixture, bound, budget):
    with pytest.raises(ValueError):
        norm_table(fixture[0], bound, max_box=budget)


def test_enumeration_accounting_and_completeness_box(fixture):
    order, _, table, resource = fixture
    assert resource == {"norm_bound": 8, "coefficient_box": 175,
                        "retained_elements": 29, "full_order_advice_used": True}
    for degree, vectors in table.items():
        assert all(norm(order, v) == degree for v in vectors)
        assert all(-v in vectors for v in vectors)


def test_identity_has_only_standard_free_factor_projectors(fixture):
    order, alpha, table, _ = fixture
    witnesses = list(unit_projectors(order, 1, zeros(4, 1), 1, table))
    assert len(witnesses) == 4
    assert len({tuple(p) for _, p in witnesses}) == 2
    assert all(not noncommuting_corners(order, alpha, p) for _, p in witnesses)


def test_hidden_advice_positive_control_is_rejected(fixture):
    order, alpha, table, _ = fixture
    beta = next(v for values in table.values() for v in values
                if order.multiply(v, alpha) != order.multiply(alpha, v))
    d = 1+norm(order, beta)
    witnesses = list(unit_projectors(order, 1, beta, d, table))
    outside = [(col, p) for col, p in witnesses if noncommuting_corners(order, alpha, p)]
    assert outside  # beta already supplies the missing noncommuting map.
    for column, _ in outside:
        with pytest.raises(ValueError, match="already leaves"):
            low_degree_witness(order, alpha, 1, beta, column)


@pytest.mark.parametrize("a,d", [(1, 49), (7, 7)])
def test_complete_square_and_small_a_certificate(fixture, a, d):
    order, alpha, table, _ = fixture
    beta = order.unit+alpha
    # Norm(beta)=48, hence a=7,d=7 gives determinant one.
    witnesses = list(unit_projectors(order, a, beta, d, table))
    if a == 1:
        assert witnesses
    for (x, y), projector in witnesses:
        z = a*x+order.multiply(beta, y)
        assert norm(order, z)+norm(order, y) == a
        witness = low_degree_witness(order, alpha, a, beta, (x, y))
        if noncommuting_corners(order, alpha, projector):
            assert witness is not None and witness["degree"] <= a
    # This tests the identity; it must not manufacture a positive native signal.
    assert not any(noncommuting_corners(order, alpha, p) for _, p in witnesses)


def test_polynomial_norm_converter_applies_to_legal_form(fixture):
    order, alpha, _, _ = fixture
    h = gram_matrix(order, 2, alpha, 24)
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    assert matrix_multiply(order, h, h)-26*h+identity == zeros(16, 1)
    record = certificate(26, 30)
    assert (record["coin_x"], record["coin_y"]) == (3, 34)
    assert all(verify_certificate(record).values())


@pytest.mark.parametrize("a,d", [(0, 1), (2, 1), (-1, -1)])
def test_nonprincipal_or_nonpositive_form_rejected(fixture, a, d):
    with pytest.raises(ValueError):
        gram_matrix(fixture[0], a, zeros(4, 1), d)


def test_rational_coefficients_not_silently_promoted(fixture):
    order, alpha, _, _ = fixture
    with pytest.raises(ValueError, match="integral quaternion"):
        gram_matrix(order, 1, Rational(1, 2)*order.unit, 1)
    with pytest.raises(ValueError, match="integral witness"):
        low_degree_witness(order, alpha, 1, alpha,
                           (Rational(1, 2)*order.unit, order.unit))


def test_scalar_mod_two_cannot_swap_distinct_product_projectors():
    e = Matrix.diag(1, 1, 0, 0)
    f = eye(4)-e
    pi = eye(4)
    assert e*f == zeros(4)
    assert (pi*e-f*pi).applyfunc(lambda v: v % 2) != zeros(4)
    # Without scalar Frobenius the local permutation obstruction disappears.
    swap = Matrix([[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]])
    assert swap*e == f*swap


@pytest.mark.parametrize("p,twisted,count", [(23, False, 46), (47, True, 76)])
def test_finite_search_scope_and_negative_controls(p, twisted, count):
    result = completion_control(characteristic=p, twisted=twisted)
    assert not result["found"]
    assert result["forms_tested"] == count
    assert result["supplied_order_control"]
    for key in ("native_geometric_decomposition", "all_polarized_decompositions_searched",
                "global_nonexistence_claim", "speedup_claim"):
        assert result[key] is False
