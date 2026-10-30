"""Arithmetic controls for the SAME native source, not native executions."""

from fractions import Fraction
from itertools import product
from pathlib import Path
import sys

import pytest
from sympy import Matrix, Rational, eye, zeros
from sympy.matrices.normalforms import hermite_normal_form

from quadratic_gate import (
    centered_division_proposal, index_prime_plan, quadratic_prime_proposal,
    query_intersection_generator,
)
from pair_order import norm, trace

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "native-nonbass-realization-2026-10-26"))
sys.path.insert(0, str(ROOT / "polarization-completion-probe-2026-10-25"))
from native_realization import rebase_order
from kernel_output import odd_maximal_order, odd_maximal_split, reconstruct
from polarization_probe import norm_table


def integral(value):
    return all(x.is_Integer is True for x in value)


@pytest.fixture(scope="module")
def neighbor():
    # The target has only scalar units, unlike the earlier p=11 fixture.
    source = odd_maximal_order(103)
    q = 5
    target_basis = reconstruct(source, odd_maximal_split(103, q),
                               Matrix([1, 0]), q).order_basis
    r_basis = Matrix.diag(1, q, q, q)
    return source, target_basis, r_basis, rebase_order(source, r_basis)


@pytest.mark.parametrize("coordinates,expected", [
    ((7, 6, -9, 3), (0, 2, -3, 1)),
    ((-2, 0, -30, 0), (0, 0, -1, 0)),
    ((0, 10, 15, 20), (0, 2, 3, 4)),
])
def test_intersection_uses_primitive_integer_coefficients(coordinates, expected):
    order = odd_maximal_order(103)
    beta = Matrix(coordinates)
    theta = query_intersection_generator(order, beta)
    assert theta == Matrix(expected)
    assert order.multiply(beta, theta) == order.multiply(theta, beta)
    for coordinates in product(range(-1, 2), repeat=4):
        x = Matrix(coordinates)
        commutes = order.multiply(x, beta) == order.multiply(beta, x)
        in_plane = Matrix.hstack(order.unit, theta, x).rank() == 2
        assert commutes == in_plane
        if in_plane:
            coefficients = Matrix.hstack(order.unit, theta).gauss_jordan_solve(x)[0]
            assert integral(coefficients)


def test_intersection_is_essential_before_using_only_index_primes():
    maximal = odd_maximal_order(103)
    beta = Matrix([2, 15, 0, 0])
    assert trace(maximal, beta)**2-4*norm(maximal, beta) == -900
    assert index_prime_plan(1, ()) == ()
    # R is already maximal: there must be no artificial 3/5 factor debt.
    assert query_intersection_generator(maximal, beta) == eye(4)[:, 1]


@pytest.mark.parametrize("index", [0, 2, 10, True])
def test_index_plan_rejects_unsaturated_or_invalid_index(index):
    with pytest.raises(ValueError, match="odd index"):
        index_prime_plan(index, ())


@pytest.mark.parametrize("index,factors", [
    (9, ((3, 1),)), (9, ((3, 1), (3, 1))), (9, ((9, 1),)),
    (9, ((3, 0),)), (9, ((True, 2),)),
])
def test_factorization_is_verified_not_assumed(index, factors):
    with pytest.raises(ValueError):
        index_prime_plan(index, factors)


@pytest.mark.parametrize("coordinate", [1, 2, 3])
def test_index_primes_suffice_without_factoring_the_whole_query_discriminant(coordinate):
    source = odd_maximal_order(103)
    r_basis = Matrix.diag(1, 15, 15, 15)
    order = rebase_order(source, r_basis)
    theta = query_intersection_generator(order, eye(4)[:, coordinate])
    plan = index_prime_plan(15**3, ((5, 3), (3, 3)))
    assert plan == ((3, 3), (5, 3))
    calls = 0
    for prime, cap in plan:
        for _ in range(cap):
            proposal = quadratic_prime_proposal(order, theta, prime)
            if proposal is None:
                break
            calls += 1
            # ONLY this test has the full native-order answer as supplied data.
            assert integral(r_basis*proposal["candidate"])
            assert proposal["native_integrality_certified"] is False
            theta = proposal["candidate"]
    assert r_basis*theta-eye(4)[:, coordinate] in (zeros(4, 1), -source.unit)
    assert calls == 2
    assert calls <= sum(cap for _, cap in plan)
    assert all(quadratic_prime_proposal(order, theta, p) is None for p, _ in plan)
    # The whole quaternion order was NOT recovered by this rank-two result.
    assert r_basis.det() == 15**3


def test_step_preserves_the_quadratic_polynomial_and_changes_index():
    order = odd_maximal_order(103)
    theta = 3*eye(4)[:, 2]+2*order.unit
    proposal = quadratic_prime_proposal(order, theta, 3)
    eta = proposal["candidate"]
    assert theta == 3*eta+proposal["shift"]*order.unit
    assert order.multiply(eta, eta) == proposal["new_trace"]*eta-proposal["new_norm"]*order.unit
    assert proposal["new_discriminant"]*9 == proposal["old_discriminant"]
    assert proposal["native_integrality_certified"] is False


def test_algebraically_integral_candidate_can_fail_native_division(neighbor):
    source, target_basis, r_basis, order = neighbor
    theta = eye(4)[:, 1]
    proposal = quadratic_prime_proposal(order, theta, 5)
    candidate = r_basis*proposal["candidate"]
    assert integral(candidate)  # Integral in the WRONG abstract center.
    assert norm(source, candidate) == 1 and trace(source, candidate) == 0
    assert not integral(target_basis.inv()*candidate)
    assert proposal["native_integrality_certified"] is False


def test_neighbor_fixture_has_no_missing_easy_unit(neighbor):
    source, target_basis, _, _ = neighbor
    target = rebase_order(source, target_basis)
    table, bounds = norm_table(target, 1)
    assert {tuple(x) for x in table[1]} == {tuple(target.unit), tuple(-target.unit)}
    assert bounds["full_order_advice_used"] is True


def test_exact_prime_division_growth_on_the_realization(neighbor):
    source, target_basis, r_basis, order = neighbor
    q = 5
    accepted = useful = 0
    for b, c, e in product(range(q), repeat=3):
        beta = Matrix([0, b, c, e])
        proposal = centered_division_proposal(order, beta, q)
        candidate = r_basis*proposal["candidate"]
        is_native = integral(target_basis.inv()*candidate)
        is_new = not integral(proposal["candidate"])
        accepted += is_native
        useful += is_native and is_new
        assert proposal["native_integrality_certified"] is False
        if is_native:
            assert norm(source, candidate).is_Integer
    assert accepted == q*q
    assert useful == q*q-1
    assert Fraction(useful, q**3) == Fraction(24, 125)
    d = q**3
    assert Fraction(useful, q**3) > Fraction(d-1, d**3) > Fraction(d-1, d**4)


@pytest.mark.parametrize("q", [3, 5, 7])
def test_residue_growth_count_is_independent_of_the_hidden_neighbor(q):
    for t in list(range(q))+[None]:
        hits = 0
        for b, c, e in product(range(q), repeat=3):
            # X=[[b,c],[e,0]], checked against v=(1,t) or v=(0,1).
            determinant = -c if t is None else e-b*t-c*t*t
            hits += determinant % q == 0 and (b, c, e) != (0, 0, 0)
        assert hits == q*q-1


def borel_fixture(q):
    source = odd_maximal_order(103)
    split = odd_maximal_split(103, q)
    row = [int(a[1, 0]) for a in split]
    pivot = next(i for i in range(4) if row[i] % q)
    inverse = pow(row[pivot], -1, q)
    columns = [q*eye(4)[:, pivot]]
    columns += [eye(4)[:, i]-(row[i]*inverse % q)*eye(4)[:, pivot]
                for i in range(4) if i != pivot]
    basis = hermite_normal_form(Matrix.hstack(*columns))
    assert basis.det() == q
    return source, basis, rebase_order(source, basis)


@pytest.mark.parametrize("d", [3, 5])
def test_centered_full_index_gate_counts_all_scalar_cosets(d):
    _, basis, order = borel_fixture(d)
    direct = centered = 0
    for coefficients in product(range(d), repeat=4):
        beta = Matrix(coefficients)
        raw = beta/d
        direct += integral(basis*raw) and not integral(raw)
        candidate = centered_division_proposal(order, beta, d)["candidate"]
        centered += integral(basis*candidate) and not integral(candidate)
    assert direct == d-1
    assert centered == d*(d-1)


def test_no_growth_quadratic_gate_forces_new_corners_to_be_transverse():
    source = odd_maximal_order(103)
    basis = Matrix.diag(1, 1, 5, 5)
    rebase_order(source, basis)
    beta = eye(4)[:, 1]
    assert all(quadratic_prime_proposal(source, beta, q) is None for q in (3, 5, 7))
    for coefficients in product(range(-1, 2), repeat=4):
        x = Matrix(coefficients)
        outside = not integral(basis.inv()*x)
        if outside:
            assert source.multiply(x, beta) != source.multiply(beta, x)
    # The scalar exception must be retained: commuting now says nothing.
    x = eye(4)[:, 2]
    assert not integral(basis.inv()*x)
    assert source.multiply(x, source.unit) == source.multiply(source.unit, x)


def test_scalar_fractional_even_and_unadapted_inputs_are_not_silently_used():
    order = odd_maximal_order(103)
    assert query_intersection_generator(order, 7*order.unit) is None
    with pytest.raises(ValueError, match="integral"):
        query_intersection_generator(order, Matrix([0, Rational(1, 2), 0, 0]))
    for bad_prime in (2, 9, True):
        with pytest.raises(ValueError, match="odd prime"):
            quadratic_prime_proposal(order, 3*eye(4)[:, 1], bad_prime)
    with pytest.raises(ValueError, match="nonscalar"):
        quadratic_prime_proposal(order, order.unit, 3)
    with pytest.raises(ValueError, match="odd divisor"):
        centered_division_proposal(order, order.unit, 2)
    permutation = eye(4)
    permutation.col_swap(0, 1)
    changed = rebase_order(order, permutation)
    with pytest.raises(ValueError, match="unit-adapted"):
        query_intersection_generator(changed, eye(4)[:, 0])
