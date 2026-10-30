from copy import deepcopy
from fractions import Fraction
from itertools import product
from math import prod

import pytest

from avoidance import greedy_avoid, solve_native
from seed_search import search
from small_prime import (BRANCHES, P, SPLITTING_X, MASKS, build_control,
                         evaluate, parameter_bounds, seed, split_fiber)
from tower_seed import verify_certificate


def test_reproducible_bounded_discovery():
    result = search(P, width=120)
    assert result["branches"] == list(BRANCHES)
    assert result["splitting_x"] == list(SPLITTING_X)
    assert result["intersections_examined"] == 235285
    assert not result["smallest_prime_claimed"]


def test_failed_search_is_not_nonexistence():
    result = search(7, width=1)
    assert result["status"] == "UNKNOWN_SEARCH_CAP"
    assert not result["nonexistence_established"]


def test_exact_seed_and_tamper():
    cert = seed().certificate()
    assert verify_certificate(cert)
    assert (cert["genus"], cert["splitting_places"], cert["schoof_squared_margin"]) == (6, 23, 4)
    cert["affine_splitting_pairs"][0]["square_roots"][0] = 0
    assert not verify_certificate(cert)


@pytest.mark.parametrize("x", SPLITTING_X+(6,))
def test_every_native_point_and_radical(x):
    points = split_fiber(x)
    assert len(points) == 16
    assert len({(point["y"], *point["w"]) for point in points}) == 16
    for point in points:
        assert point["y"]**2 % P == prod(x-a for a in BRANCHES) % P
        for i, w in enumerate(point["w"], 1):
            assert w*w % P == (x-BRANCHES[0])*(x-BRANCHES[i]) % P
        for mask in MASKS:
            assert evaluate((mask, 0), point)**2 % P == prod(
                x-a for i, a in enumerate(BRANCHES) if mask & (1 << i)) % P


def test_all_radical_products_retain_relative_signs():
    for x in SPLITTING_X+(6,):
        for point in split_fiber(x):
            values = {mask: evaluate((mask, 0), point) for mask in MASKS}
            for left, right in product(MASKS, repeat=2):
                common = prod(x-a for i,a in enumerate(BRANCHES)
                              if left & right & (1 << i)) % P
                assert values[left]*values[right] % P == common*values[left ^ right] % P


def test_native_matrix_is_complete_and_cubic_attack_is_absent():
    problem, _, data = build_control()
    assert (problem.k, problem.m, len(problem.W), len(problem.U)) == (43, 176, 126, 176)
    assert not problem.annihilator
    assert data["dimension_L_G_minus_K"] == 0
    for coefficients in data["rr_basis"]:
        for constraint in data["constraints"]:
            assert sum(a*b for a, b in zip(coefficients, constraint)) % P == 0
    assert not data["uniform_divisor_class_sample"]
    assert not data["native_higher_levels_constructed"]
    assert not data["quantum_advantage_established"]


def test_extra_fiber_is_not_falsely_certified_full_kummer_split():
    assert len(split_fiber(6)) == 16
    assert any(pow((6-a) % P, (P-1)//2, P) != 1 for a in BRANCHES)


def test_same_native_input_classically_solved_all_basis_targets():
    problem, fiber, data = build_control()
    targets = [(0,)*43, (1,)*43, tuple(range(43))]
    targets += [tuple(int(i == j) for i in range(43)) for j in range(43)]
    for t, target in enumerate(targets):
        output = solve_native(P, data["original_parity"], target)
        assert problem.verifies(output["witness"], target)
        assert not output["uniform_sampler"]
        sampled = fiber.sample(target, seed=20261027+t, attempts=16)
        assert problem.verifies(sampled["witness"], target)


@pytest.mark.parametrize("e", [8, 16, 32])
def test_conditional_bounds_retain_all_cost_and_scope_flags(e):
    data = parameter_bounds(P, e)
    assert 0 < data["decoder_error_upper"] < Fraction(256, P**7)
    assert 0 < data["raw_verified_quantum_success_lower"] < 1
    assert data["prime_count_condition"]
    assert data["bad_prime_upper"] < Fraction(1, 10**58)
    assert data["bad_prime_one_degree_ratio_upper"] < 1
    error = data["decoder_error_upper"]
    tail = data["systematic"]["tail_upper"]
    assert data["raw_verified_quantum_success_lower"] == (1-error)**2/(1+tail)
    assert not data["native_matrix_generated_by_this_function"]
    assert not data["quantum_advantage_established"]


@pytest.mark.parametrize("p,e", [(43,8), (1019,4), (1019,12), (1023,8)])
def test_invalid_parameter_promises_rejected(p, e):
    with pytest.raises(ValueError):
        parameter_bounds(p, e)


def test_greedy_native_exhaustive_small_control():
    parity = [[1,0,1,1], [0,1,1,2]]
    for target in product(range(5), repeat=2):
        result = solve_native(5, parity, target)
        word = result["witness"]
        assert all(word)
        assert [sum(a*b for a,b in zip(row, word)) % 5 for row in parity] == list(target)


def test_greedy_dead_end_is_not_empty_fiber():
    # The first legal choice x_0=1 makes both nonzero x_1 values forbidden.
    matrix, target = [[1,1], [0,1]], [2,2]
    output = greedy_avoid(matrix, target, 3)
    assert output["status"] == "UNKNOWN_GREEDY_DEAD_END"
    assert not output["infeasibility_established"]
    x = [2,1]
    assert all(x)
    assert all(sum(a*b for a,b in zip(row,x)) % 3 != t for row,t in zip(matrix,target))


def test_no_second_basis_is_not_unsatisfiable():
    result = solve_native(5, [[1,0]], [1])
    assert result["status"] == "UNKNOWN_NO_SECOND_BASIS"
    assert not result["infeasibility_established"]


def test_malformed_native_inputs_rejected():
    with pytest.raises(ValueError):
        solve_native(5, [[1,1]], [5])
    with pytest.raises(ValueError):
        solve_native(5, [[1,1],[1,1]], [1,1])


def test_witness_checked_against_original_target():
    _, fiber, data = build_control()
    result = solve_native(P, data["original_parity"], [0]*43)
    word = deepcopy(result["witness"])
    word[0] = 0
    assert not fiber.verifies(word, [0]*43)
    assert not fiber.verifies(result["witness"], [1]*43)
