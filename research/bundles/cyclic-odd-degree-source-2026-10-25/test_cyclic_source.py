from math import gcd, prod
from pathlib import Path
from random import Random
import sys

import pytest
from sympy import Matrix, eye, zeros

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cyclic_source import (
    affine_query, certificate_queries, checked_factors, combine_local_lines,
    crt_query, cyclic_annihilator,
    odd_ring_lift, primitive_frame, sl_ring_word, uniform_plan,
)
from controls_cyclic import (
    cyclic_degree25_control, local_lines, preserves_doubled, split_fixture, square_phase_control,
)
from kernel_output import (
    action, alternating_form, check_split, matrix_multiply, mod,
    odd_maximal_order, product_actions,
)
from uniform_source_bound import elementary


def multiply_word(word, d, n):
    result = eye(d)
    for i, j, c in word:
        result = mod(result*elementary(d, i, j, c), n)
    return result


def test_nonzero_is_not_unit_pivot():
    matrix = Matrix([[3, 1], [5, 2]])
    assert matrix.det() == 1
    assert gcd(3, 15) > 1 and gcd(5, 15) > 1
    word = sl_ring_word(matrix, 15, ((3, 1), (5, 1)))
    assert multiply_word(word, 2, 15) == matrix
    assert len(word) <= 9


@pytest.mark.parametrize("n,factors", [(9, ((3, 2),)), (15, ((3, 1), (5, 1))),
                                      (25, ((5, 2),)), (45, ((3, 2), (5, 1))),
                                      (343, ((7, 3),))])
@pytest.mark.parametrize("seed", [0, 8])
def test_ring_lift_same_query_inverse_parity_bound(n, factors, seed):
    order = odd_maximal_order(11)
    split = split_fixture(11, n, factors)
    check_split(order, split, n)
    rng, matrix, form = Random(seed), eye(4), alternating_form(2)
    for _ in range(5):
        v = Matrix([rng.randrange(n) for _ in range(4)])
        matrix = mod(matrix*(eye(4)+v*v.T*form), n)
    physical = sl_ring_word(matrix, n, factors)
    assert multiply_word(physical, 4, n) == matrix
    result = odd_ring_lift(order, split, matrix, n, factors)
    sigma, inverse, s, t = (result[k] for k in ("sigma", "inverse", "S", "trace"))
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    assert matrix_multiply(order, sigma, inverse) == identity
    assert matrix_multiply(order, inverse, sigma) == identity
    assert mod(action(sigma, product_actions(split)), n) == matrix
    assert mod(s-identity, n) == zeros(16, 1)
    assert matrix_multiply(order, s, s)-t*s+identity == zeros(16, 1)
    tau = identity.copy()
    tau[4:8, :] = order.unit
    assert mod(sigma-tau, 2) == zeros(16, 1)
    plan = uniform_plan(order, n, factors, 11)
    assert 3 <= t <= plan["trace_bound"] and t % 2 == 1
    assert result["physical_length"] <= 36
    assert len(result["quaternion_factors"]) <= 145
    assert plan["multiplier"] > plan["trace_bound"]**2
    assert plan["multiplier"] == prod(plan["quotient_primes"])
    assert all(gcd(r, n*11) == 1 and r % 2 for r in plan["weak_query_orders"])
    assert len(set(plan["weak_query_orders"])) == len(plan["weak_query_orders"])
    assert plan["marking_product"]**2 > plan["marking_threshold_squared"]


@pytest.mark.parametrize("p,e", [(3, 1), (3, 2), (3, 3), (5, 2), (7, 2)])
def test_two_full_source_checks_certify_exact_local_line(p, e):
    m, factors = p**e, ((p, e),)
    form = alternating_form(2)
    for candidate in ((1, 0), (0, 1), (1, p), (2, 1)):
        queries = certificate_queries(candidate, m, factors)
        assert all(mod(q.T*form*q-form, m) == zeros(4) for q in queries)
        accepted = [v for v in local_lines(p, e)
                    if all(preserves_doubled(q, v, m) for q in queries)]
        assert len(accepted) == 1
        x, y = candidate
        assert (x*accepted[0][1]-y*accepted[0][0]) % m == 0


def test_SL2_stabilizers_collide_at_nine_but_full_source_certificates_do_not():
    # Equal SL2 stabilizers do not identify the point over this local ring.
    sets = []
    for x, y in ((1, 0), (1, 3), (1, 6)):
        stabilizer = set()
        for a in range(9):
            for b in range(9):
                for c in range(9):
                    for d in range(9):
                        if (a*d-b*c) % 9 == 1 and (x*(c*x+d*y)-y*(a*x+b*y)) % 9 == 0:
                            stabilizer.add((a, b, c, d))
        sets.append(stabilizer)
    assert len(sets[0]) == 54 and sets[0] == sets[1] == sets[2]
    checks = certificate_queries((1, 0), 9, ((3, 2),))
    assert all(preserves_doubled(q, (1, 0), 9) for q in checks)
    assert preserves_doubled(checks[0], (1, 3), 9)
    assert not preserves_doubled(checks[1], (1, 3), 9)


@pytest.mark.parametrize("p,e", [(3, 1), (3, 2), (3, 3), (5, 1), (5, 3), (7, 2)])
def test_local_square_unit_phase_peak(p, e):
    record = square_phase_control(p, e, 2, 4)
    assert record["square_unit_count"] == p**(e-1)*(p-1)//2
    assert record["correct_probability"] == pytest.approx((p-1)/(2*p))
    assert record["normalization"] == pytest.approx(1)
    assert not record["quantum_execution"]


def test_global_square_unit_sampling_loses_exponentially_in_factor_count():
    primes = (3, 5, 7, 13)
    n = prod(primes)
    square_count = prod((p-1)//2 for p in primes)
    unit_count = prod(p-1 for p in primes)
    assert square_count*2**len(primes) == unit_count
    assert square_count/n < 1/16


@pytest.mark.parametrize("m", [3, 9, 25, 27])
def test_public_affine_queries_have_claimed_fibers_without_using_slope(m):
    for a in (1, 2, m-1):
        for u in (0, 1, m-1):
            query = affine_query(a, u, m)
            assert int(query.det()) % m == 1
            assert mod(affine_query(-a, u, m)+query, m) == zeros(2)
            for z in (0, 1, m-1):
                assert mod(a*query*Matrix([z, 1]), m) == Matrix([(a*a*z+u) % m, 1])


def test_local_chart_outputs_combine_without_a_global_unit_coordinate():
    vector = combine_local_lines(15, ((3, 1), (5, 1)), [(0, 1), (1, 0)])
    assert list(vector) == [6, 10]
    assert gcd(int(vector[0]), 15) > 1 and gcd(int(vector[1]), 15) > 1
    assert int(primitive_frame(vector, 15, ((3, 1), (5, 1))).det()) % 15 == 1


def test_full_certificate_over_mixed_primary_components():
    candidate, n = (3, 5), 15
    queries = certificate_queries(candidate, n, ((3, 1), (5, 1)))
    accepted = []
    for x in range(n):
        for y in range(n):
            if gcd(x, y, n) == 1:
                result = all(preserves_doubled(q, (x, y), n) for q in queries)
                assert result == ((3*y-5*x) % n == 0)
                if result:
                    accepted.append((x, y))
    assert len(accepted) == 8


def test_cyclic_degree25_algebraic_isogeny_source_control():
    record = cyclic_degree25_control()
    assert record["elliptic_degree"] == 25 and record["phi_mod5_rank"] == 1
    assert len(record["local_kernels"]) == 7
    assert not record["curve_points_generated"] and not record["quotient_executed"]


def test_crt_queries_and_cyclic_annihilator_with_no_global_unit_coordinate():
    n, factors, vector = 15, ((3, 1), (5, 1)), Matrix([3, 5])
    frame = primitive_frame(vector, n, factors)
    assert int(frame.det()) % n == 1
    assert gcd(3, 15) > 1 and gcd(5, 15) > 1
    local = certificate_queries((2, 1), 3, ((3, 1),))[1]
    lifted = crt_query(local, 3, n)
    assert mod(lifted, 3) == mod(local, 3)
    assert mod(lifted, 5) == eye(4)
    assert mod(lifted.T*alternating_form(2)*lifted-alternating_form(2), n) == zeros(4)
    order, split = odd_maximal_order(11), split_fixture(11, n, factors)
    ideal = cyclic_annihilator(order, split, vector, n, factors)
    assert abs(ideal.det()) == n*n
    assert all(x.q == 1 for x in ideal.inv()*(n*eye(4)))
    for i in range(4):
        assert mod(action(ideal[:, i], split)*vector, n) == zeros(2, 1)
        for j in range(4):
            assert all(x.q == 1 for x in
                       ideal.inv()*order.multiply(eye(4)[:, j], ideal[:, i]))


@pytest.mark.parametrize("n,factors", [(9, ((3, 1),)), (9, ((3, 1), (3, 1))),
                                      (10, ((2, 1), (5, 1))), (9, ((9, 1),))])
def test_wrong_factorization_rejected(n, factors):
    with pytest.raises(ValueError):
        checked_factors(n, factors)


def test_noncyclic_and_noncomponent_shortcuts_rejected():
    with pytest.raises(ValueError, match="primitive"):
        primitive_frame((3, 3), 9, ((3, 2),))
    with pytest.raises(ValueError):
        crt_query(eye(4), 3, 9)
    with pytest.raises(ValueError):
        uniform_plan(odd_maximal_order(11), 33, ((3, 1), (11, 1)), 11)
    with pytest.raises(ValueError):
        odd_ring_lift(odd_maximal_order(11), split_fixture(11, 9, ((3, 2),)),
                      2*eye(4), 9, ((3, 2),))
