from pathlib import Path
from random import Random
import sys

import pytest
from sympy import Matrix, eye, zeros

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_split import SearchBudgetExceeded, source_split, square_root
from double_level_source import extend_split_to_double
from kernel_output import QuaternionOrder, action, check_split, mod, odd_maximal_order, odd_maximal_split, reconstruct


@pytest.mark.parametrize("prime", [3, 5, 7, 13, 17, 65537, 1000000007, 1000000009])
def test_large_and_small_prime_splits(prime):
    order = odd_maximal_order(11)
    actions, costs = source_split(order, prime, [(prime, 1)], 11, Random(17))
    check_split(order, actions, prime)
    assert costs["prime_powers"][0]["semisimple_draws"] <= 64
    assert not costs["large_prime_element_enumeration"]
    assert not costs["native_torsion_used"] and not costs["target_order_used"]


@pytest.mark.parametrize("prime,exponent", [(2, 1), (2, 5), (3, 4), (5, 3), (65537, 2)])
def test_precision_lifting_preserves_coordinates(prime, exponent):
    order = odd_maximal_order(11)
    base, _ = source_split(order, prime, [(prime, 1)], 11, Random(9))
    full, _ = source_split(order, prime**exponent, [(prime, exponent)], 11, Random(9))
    assert all(mod(a-b, prime) == zeros(2) for a, b in zip(base, full))
    check_split(order, full, prime**exponent)
    doubled = extend_split_to_double(order, full, prime**exponent)
    assert all(mod(a-b, prime**exponent) == zeros(2) for a, b in zip(full, doubled))


def test_composite_crt_and_source_pipeline():
    order = odd_maximal_order(11)
    n = 8*9*25
    actions, _ = source_split(order, n, [(2, 3), (3, 2), (5, 2)], 11, Random(31))
    check_split(order, actions, n)
    double = extend_split_to_double(order, actions, n)
    check_split(order, double, 2*n)


def test_nonstandard_integral_source_basis():
    old = odd_maximal_order(11)
    change = Matrix([[0, 1, 2, 0], [1, 0, 0, 0], [0, 0, 1, 1], [0, 0, 0, 1]])
    inverse = change.inv()
    order = QuaternionOrder(
        tuple(tuple(inverse*old.multiply(change[:, i], change[:, j]) for j in range(4))
              for i in range(4)), inverse*old.unit,
        inverse*old.involution*change, old.traces*change)
    actions, _ = source_split(order, 17**3, [(17, 3)], 11, Random(29))
    assert mod(action(order.unit, actions), 17**3) == eye(2)
    check_split(order, actions, 17**3)


def test_changed_coordinates_give_same_output_order():
    order = odd_maximal_order(11)
    old = odd_maximal_split(11, 5)
    new, _ = source_split(order, 5, [(5, 1)], 11, Random(18))
    alpha = order.unit+2*eye(4)[:, 1]
    recovered = []
    for actions in (old, new):
        matrix = mod(action(alpha, actions), 5)
        row = next(matrix[i, :] for i in range(2) if matrix[i, :] != zeros(1, 2))
        kernel = mod(Matrix([-row[1], row[0]]), 5)
        assert mod(matrix*kernel, 5) == zeros(2, 1)
        recovered.append(reconstruct(order, actions, kernel, 5).order_basis)
    assert recovered[0] == recovered[1]


class OnlyZero:
    def randrange(self, *args):
        return 0 if len(args) == 1 else 1


def test_budget_exhaustion_is_unknown_not_nonsplitting():
    with pytest.raises(SearchBudgetExceeded, match="UNKNOWN"):
        source_split(odd_maximal_order(11), 1000000007, [(1000000007, 1)], 11,
                     OnlyZero(), trials=3)
    with pytest.raises(SearchBudgetExceeded, match="nonresidue"):
        square_root(4, 17, OnlyZero(), 3)


@pytest.mark.parametrize("p", [3, 5, 17, 65537, 1000000009])
def test_square_root_verifies_exactly(p):
    for x in (0, 1, 2, 12345 % p):
        root, _ = square_root(x*x % p, p, Random(19), 64)
        assert root*root % p == x*x % p


@pytest.mark.parametrize("n,factors", [(11, [(11, 1)]), (15, [(3, 1)]), (9, [(9, 1)])])
def test_invalid_level_contract_rejected(n, factors):
    with pytest.raises(ValueError):
        source_split(odd_maximal_order(11), n, factors, 11, Random(1))
