from copy import deepcopy
from math import gcd, prod
from pathlib import Path
from random import Random
import sys

import pytest
from sympy import Matrix, eye, zeros

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prime_source import (
    odd_trace_bound, odd_trace_lift, prime_certificate, prime_coin_witness,
    prime_resource_plan, verify_prime_certificate,
)
from kernel_output import (
    action, alternating_form, matrix_multiply, mod, odd_maximal_order,
    odd_maximal_split, product_actions,
)
from controls_prime_source import integral_control


@pytest.mark.parametrize("ell", [3, 5, 13])
@pytest.mark.parametrize("seed", [0, 7])
def test_same_query_integral_inverse_odd_trace_and_uniform_bound(ell, seed):
    rng, order = Random(seed), odd_maximal_order(11)
    split, j = odd_maximal_split(11, ell), alternating_form(2)
    query = eye(4)
    for _ in range(4):
        v = Matrix([rng.randrange(ell) for _ in range(4)])
        query = mod(query*(eye(4)+v*v.T*j), ell)
    lifted = odd_trace_lift(order, split, query, ell)
    sigma, inverse, s, t = (lifted[key] for key in ("sigma", "inverse", "S", "trace"))
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    tau = identity.copy()
    tau[4:8, :] = order.unit
    assert mod(sigma-tau, 2) == zeros(16, 1)
    assert matrix_multiply(order, sigma, inverse) == identity
    assert matrix_multiply(order, inverse, sigma) == identity
    assert mod(action(sigma, product_actions(split)), ell) == query
    assert mod(s-identity, ell) == zeros(16, 1)
    assert matrix_multiply(order, s, s)-t*s+identity == zeros(16, 1)
    bound = odd_trace_bound(order, ell)
    assert 3 <= t <= bound["trace_bound"] and t % 2 == 1
    assert lifted["quaternion_length"] <= bound["quaternion_length_bound"] == 157
    for _, _, q in lifted["factors"][:-1]:
        assert all(int(x) % 2 == 0 and abs(x) <= ell-1 for x in q)
    assert lifted["factors"][-1][2] == ell*order.unit


@pytest.mark.parametrize("t", [3, 5, 7, 9, 27, 101])
def test_certificate_uses_N_not_N_squared(t):
    plan = prime_resource_plan(t, 61, 103)
    record = prime_certificate(t, plan["multiplier"])
    assert all(verify_prime_certificate(record).values())
    assert record["multiplier"] == prod(plan["quotient_primes"])
    assert (t+2)*record["coin_x"]+(t-2)*record["coin_y"] == record["multiplier"]


def test_prime_kernels_and_ramified_quadratic_prime():
    record = integral_control()
    assert record["local_kernels"][-1] == {
        "prime": 29, "kernel_dimension": 16, "F_rank": 16, "isotropic": True,
        "quadratic_discriminant_zero": True,
    }
    assert record["common_mask_preserved"]
    assert record["wrong_squared_inverse_rejected"]
    assert not record["geometric_points_generated"]
    assert not record["quotient_executed"]


@pytest.mark.parametrize("bits", [8, 128, 1024])
def test_global_plan_requires_only_distinct_odd_primes(bits):
    t, ell, p = 2**bits+1, 2**127-1, 103
    plan = prime_resource_plan(t, ell, p)
    primes, marks = plan["quotient_primes"], plan["marking_primes"]
    n = plan["multiplier"]
    assert n == prod(primes) and n > t*t
    assert n % 2 == 1 and gcd(n, ell*p) == 1
    assert len(set(primes+marks)) == len(primes+marks)
    assert set(primes).isdisjoint(marks)
    assert plan["weak_evaluation_orders"] == primes+marks
    assert plan["quotient_torsion_exponent"] == 1
    assert plan["marking_product"]**2 > plan["marking_threshold_squared"]
    assert all(plan["auxiliary_field_degree_bounds"][str(r)] == r-1 for r in primes+marks)
    assert max(primes) < 100*bits
    assert plan["theta_level_four_still_required"]
    assert not plan["geometric_backend_executed"]
    assert not plan["quantum_execution"]
    assert not plan["speedup_established"]


def test_even_trace_obstruction_is_real_not_validation_convention():
    assert gcd(4+2, 4-2) == 2 and 105 % 2 == 1
    with pytest.raises(ValueError, match="odd integer trace"):
        prime_coin_witness(4, 105)


def test_appending_a_shear_without_evenizing_the_old_lift_fails():
    ell = 5
    tau = Matrix([[1, ell], [0, 1]])
    assert mod(tau, ell) == eye(2)
    assert (tau.T*tau).trace() % 2 == 1
    assert ((tau*tau).T*(tau*tau)).trace() % 2 == 0


def test_square_target_does_not_certify_prime_only_access():
    # Formal identities are valid with a repeated prime, but the resource
    # plan is what licenses prime-only kernels. Do not conflate the two.
    record = prime_certificate(3, 25)
    assert all(verify_prime_certificate(record).values())
    assert prime_resource_plan(3, 5, 11)["multiplier"] != 25


def test_corrupt_coefficient_certificate_rejected():
    record = deepcopy(prime_certificate(7, 105))
    c = [list(row) for row in record["C"]]
    c[0][0] += 1
    record["C"] = tuple(tuple(row) for row in c)
    assert not all(verify_prime_certificate(record).values())


@pytest.mark.parametrize("t,n", [(True, 105), (7, 30), (7, 3), (2, 105)])
def test_bad_coin_contract(t, n):
    with pytest.raises(ValueError):
        prime_coin_witness(t, n)


def test_wrong_dimension_not_a_general_polarization_converter():
    order = odd_maximal_order(11)
    with pytest.raises(ValueError, match="surface-only"):
        odd_trace_lift(order, odd_maximal_split(11, 5), eye(6), 5)


def test_bad_field_and_nonprime_scope():
    for ell, p in ((5, 5), (5, 3), (2, 11), (9, 11), (5, 15)):
        with pytest.raises(ValueError):
            prime_resource_plan(7, ell, p)
