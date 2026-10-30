from random import Random

import pytest
from sympy import Matrix, eye, zeros

from kernel_output import (
    action, alternating_form, matrix_multiply, matrix_star, mod,
    odd_maximal_order, odd_maximal_split, product_actions,
)
from uniform_source_bound import elementary, lift_symplectic, sl_word, smooth_denominator, uniform_surface_bound


@pytest.mark.parametrize("ell", [3, 5, 13])
@pytest.mark.parametrize("seed", [0, 1, 7])
def test_uniform_compiler_and_norm_bound(ell, seed):
    rng, order = Random(seed), odd_maximal_order(11)
    split, form = odd_maximal_split(11, ell), alternating_form(2)
    m = eye(4)
    for _ in range(7):
        v = Matrix([rng.randrange(ell) for _ in range(4)])
        m = mod(m*(eye(4)+rng.randrange(ell)*v*v.T*form), ell)
    word = sl_word(m, ell)
    product = eye(4)
    for i, j, c in word:
        product = mod(product*elementary(4, i, j, c), ell)
    assert product == m
    record = lift_symplectic(order, split, m, ell)
    sigma = record["sigma"]
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    assert matrix_multiply(order, sigma, record["inverse"]) == identity
    assert mod(action(sigma, product_actions(split)), ell) == m
    s = matrix_multiply(order, matrix_star(order, sigma), sigma)
    trace = (order.traces*(s[:4, :]+s[12:16, :]))[0]/2
    bound = uniform_surface_bound(order, ell)
    assert 2 <= trace <= bound["trace_bound"]
    assert record["physical_length"] <= 39
    assert record["quaternion_length"] <= 156
    assert all(abs(x) <= (ell-1)//2 for _, _, q in record["factors"] for x in q)
    assert all(int(x) % ell == 0 for x in s-identity)
    assert matrix_multiply(order, s, s)-trace*s+identity == zeros(16, 1)


def test_same_public_bound_for_all_queries_and_one_even_squarefree_denominator():
    order = odd_maximal_order(11)
    record = smooth_denominator(order, 13, 11)
    assert record["basis_norm_sum"] == 8
    assert record["trace_bound"] == 1154**156
    assert record["denominator"] > record["trace_bound"]+2
    assert record["denominator"] % 2 == 0
    assert 11 not in record["primes"] and 13 not in record["primes"]
    assert len(record["primes"]) == len(set(record["primes"]))
    value = 1
    for r in record["primes"]:
        value *= r
    assert value == record["denominator"]
    assert (value//record["primes"][-1]) <= record["trace_bound"]+2


def test_contract_failures():
    order = odd_maximal_order(11)
    with pytest.raises(ValueError, match="SL"):
        sl_word(Matrix.diag(2, 1, 1, 1), 5)
    with pytest.raises(ValueError, match="symplectic"):
        lift_symplectic(order, odd_maximal_split(11, 5), elementary(4, 0, 2, 1), 5)
    with pytest.raises(ValueError, match="two elliptic"):
        lift_symplectic(order, odd_maximal_split(11, 5), eye(2), 5)
    with pytest.raises(ValueError, match="characteristic"):
        smooth_denominator(order, 13, 13)
