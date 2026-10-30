from pathlib import Path
from random import Random
import sys

import pytest
from sympy import Matrix, eye, zeros

sys.path.insert(0, str(Path(__file__).resolve().parent))
from double_level_source import (
    congruence_lift, extend_split_to_double, lift_dyadic_split, resource_plan,
    sl_word, split_at_two, symplectic_double_lift,
)
from controls_double import (
    classical_control, even_isogeny_control, full_split_fixture,
    mixed_even_ideal_control, preserves_kernel,
)
from half_norm import HalfQuadratic, half_certificate, verify_half_certificate
from local_baseline import (
    classical_local_direction, content_depth, kernel_ideal_from_local_data, prefix_queries,
)
from kernel_output import (
    action, alternating_form, check_split, hurwitz_order, matrix_multiply, matrix_star,
    mod, odd_maximal_order, product_actions,
)
from uniform_source_bound import elementary


@pytest.mark.parametrize("p", [7, 11, 19, 23])
def test_generic_dyadic_order_split_and_coordinate_preserving_lifts(p):
    order = odd_maximal_order(p)
    split = split_at_two(order)
    for modulus in (2, 4, 8, 16):
        check_split(order, split, modulus)
        lifted = lift_dyadic_split(order, split, modulus)
        assert all(mod(a-b, modulus) == zeros(2) for a, b in zip(lifted, split))
        split = lifted


def test_ramified_two_order_is_not_granted_a_split():
    with pytest.raises(ValueError, match="split reduction"):
        split_at_two(hurwitz_order())


@pytest.mark.parametrize("n,factors", [(2, ((2, 1),)), (4, ((2, 2),)), (6, ((2, 1), (3, 1))),
                                      (8, ((2, 3),)), (12, ((2, 2), (3, 1))),
                                      (18, ((2, 1), (3, 2))), (5, ((5, 1),)),
                                      (9, ((3, 2),)), (15, ((3, 1), (5, 1)))])
@pytest.mark.parametrize("seed", [0, 4])
def test_same_query_integral_inverse_gram_congruence_and_bound(n, factors, seed):
    order, rng, form = odd_maximal_order(11), Random(seed), alternating_form(2)
    split = full_split_fixture(11, n, factors)
    doubled = extend_split_to_double(order, split, n)
    assert all(mod(a-b, n) == zeros(2) for a, b in zip(doubled, split))
    query = eye(4)
    for _ in range(4):
        v = Matrix([rng.randrange(n) for _ in range(4)])
        query = mod(query*(eye(4)+v*v.T*form), n)
    result = congruence_lift(order, split, query, n, factors)
    sigma, inverse, s, t = (result[k] for k in ("sigma", "inverse", "S", "trace"))
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    assert matrix_multiply(order, sigma, inverse) == identity
    assert matrix_multiply(order, inverse, sigma) == identity
    assert mod(action(sigma, product_actions(split)), n) == query
    assert mod(action(sigma, product_actions(doubled)), 2*n) == result["doubled_query"]
    assert mod(s-identity, 2*n) == zeros(16, 1)
    assert matrix_multiply(order, s, s)-t*s+identity == zeros(16, 1)
    assert t >= 2 and t % 4 == 2
    assert result["physical_length"] <= 36 and len(result["quaternion_factors"]) <= 144
    assert all(abs(x) <= n for _, _, q in result["quaternion_factors"] for x in q)
    plan = resource_plan(order, n, factors, 11)
    assert t <= plan["trace_bound"] and plan["multiplier"] > plan["trace_bound"]**2
    assert all(r % 2 and (n*11) % r for r in plan["quotient_primes"]+plan["marking_primes"])
    assert plan["marking_product"]**2 > plan["marking_threshold_squared"]


def test_double_lift_is_not_naive_integer_reduction():
    n, form = 2, alternating_form(2)
    query = Matrix([[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    assert mod(query.T*form*query-form, n) == zeros(4)
    assert mod(query.T*form*query-form, 2*n) != zeros(4)
    lifted = symplectic_double_lift(query, n)
    assert mod(lifted-query, n) == zeros(4)
    assert mod(lifted.T*form*lifted-form, 2*n) == zeros(4)


def test_even_composite_unit_pivot_word():
    matrix, n = Matrix([[2, 1], [3, 2]]), 6
    result = eye(2)
    for i, j, c in sl_word(matrix, n, ((2, 1), (3, 1))):
        result = mod(result*elementary(2, i, j, c), n)
    assert result == matrix


@pytest.mark.parametrize("trace", [2, 6, 10, 18, 42, 178])
def test_half_norm_exact_formal_identities_including_trace_two(trace):
    record = half_certificate(trace, trace*trace+1)
    assert all(verify_half_certificate(record).values())


def test_wrong_half_norm_and_missing_divisibility_are_not_silently_allowed():
    for trace in (1, 3, 4, 8):
        with pytest.raises(ValueError):
            half_certificate(trace, 10001)
    with pytest.raises(ValueError):
        HalfQuadratic(0, 1/2)
    # Even a valid mod-n lift need not make the CONJUGATED half integral.
    order = odd_maximal_order(11)
    q = eye(4)[:, 2]-eye(4)[:, 1]
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    sigma = identity.copy()
    sigma[4:8, :] = 2*q
    s = matrix_multiply(order, matrix_star(order, sigma), sigma)
    assert mod(s-identity, 2) == zeros(16, 1)
    alpha = order.unit+eye(4)[:, 1]
    phi = Matrix.vstack(alpha, zeros(4, 1), zeros(4, 1), alpha)
    h = matrix_multiply(order, matrix_multiply(order, phi, s), matrix_star(order, phi))/2
    t = (order.traces*(h[:4, :]+h[12:, :]))[0]/2
    assert t == 18 and all(x.q == 1 for x in h)
    assert any(x.q != 1 for x in (h-identity)/2)


@pytest.mark.parametrize("n,factors", [(2, ((2, 1),)), (6, ((2, 1), (3, 1))), (9, ((3, 2),))])
def test_identity_lift_really_exercises_trace_two(n, factors):
    order = odd_maximal_order(11)
    result = congruence_lift(order, full_split_fixture(11, n, factors), eye(4), n, factors)
    assert result["trace"] == 2 and result["physical_length"] == 0
    assert all(verify_half_certificate(half_certificate(2, 15)).values())


def test_actual_even_degree_map_uses_only_odd_weak_levels():
    result = even_isogeny_control()
    assert result["degree"] == 2 and result["integral_half_polarization"]
    assert all(r % 2 for r in result["weak_query_orders"])
    assert any(r["nonsemisimple"] for r in result["local_kernels"])
    assert not result["geometric_quotients_executed"]


@pytest.mark.parametrize("p,e,a", [(2, 1, 0), (2, 2, 0), (2, 2, 1), (2, 4, 1),
                                  (2, 6, 1), (2, 8, 3), (3, 5, 1), (5, 3, 0)])
def test_matched_classical_baseline_recovers_small_prime_directions(p, e, a):
    for vector in ((1, 0), (0, 1), (1, p), (p, 1), (3, 1)):
        result = classical_control(p, e, a, vector)
        direction = result["direction"]
        if direction is not None:
            assert direction["source_comparisons"] == 2*(p*(e-2*a)+1)
        assert not result["native_source_executed"]


@pytest.mark.parametrize("p,e,a", [(2, 4, 0), (2, 6, 1), (3, 4, 1)])
def test_prefix_certificates_depend_only_on_requested_digits(p, e, a):
    depth = e-2*a
    for digits in range(1, depth+1):
        queries = prefix_queries((1, p), p, e, depth, digits)
        form = alternating_form(2)
        assert all(mod(q.T*form*q-form, p**e) == zeros(4) for q in queries)
        for z in range(p**depth):
            assert all(preserves_kernel(q, p, e, a, (1, z)) for q in queries) == (
                (z-p) % (p**digits) == 0)


def test_classical_query_budget_is_charged_before_calls():
    calls = []
    with pytest.raises(ValueError, match="budget"):
        classical_local_direction(1009, 3, 3, lambda q: calls.append(q), max_queries=4096)
    assert not calls
    with pytest.raises(ValueError, match="unique"):
        classical_local_direction(2, 2, 2, lambda q: True)
    with pytest.raises(ValueError, match="boolean"):
        content_depth(2, 2, lambda q: 1)


def test_mixed_even_noncyclic_kernel_ideal_is_the_original_one():
    result = mixed_even_ideal_control()
    assert result["degree"] == 200 and result["ideal_index"] == 200**2
    assert result["ideal_equals_original_principal_left_ideal"]


def test_entirely_scalar_even_kernel_and_invalid_direction_data():
    order, factors = odd_maximal_order(11), ((2, 2), (3, 2))
    actions = full_split_fixture(11, 36, factors)
    assert kernel_ideal_from_local_data(order, actions, 36, factors, {2: 1, 3: 1}, {}) == 6*eye(4)
    with pytest.raises(ValueError, match="exactly match"):
        kernel_ideal_from_local_data(order, actions, 36, factors, {2: 1, 3: 1}, {2: (1, 0)})
