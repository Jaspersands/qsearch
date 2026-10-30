from fractions import Fraction as F
from itertools import product
import random

import pytest

from four_list import (binary_rank, exact_mixture_moments, exact_uniform_moments,
                       four_list_match, mixture_joint_probability,
                       overlap_certificate, tower_certificate)


def test_every_overlap_and_support_scale_is_bounded():
    result = overlap_certificate()
    assert result["checked_support_masks"] == 1296
    assert all(row["maximum_scale_exponent"] == 0 for row in result["cases"])
    assert result["untruncated_success_lower"] > F(1, 4000)
    assert result["untruncated_success_lower"]-F(5, 40000) > result["capped_success_lower"]


@pytest.mark.parametrize("e,expected", [(8, False), (16, False), (32, False), (64, True), (128, True)])
def test_native_degree_budget_and_exact_bias_cutoffs(e, expected):
    data = tower_certificate(e)
    assert sum(data["four_prime_degrees"]) == 2*e-9
    assert data["four_list_guarantee_under_access_contract"] == expected
    assert data["rank_is_worst_case_upper_not_measured"]
    assert not data["actual_auxiliary_divisor_constructed"]
    assert not data["polynomial_time_for_linear_rank"]


def test_e64_exact_initial_inequality():
    data = tower_certificate(64)
    assert data["four_prime_degrees"] == [29, 30, 30, 30]
    assert data["list_length_exponent"] == 214
    assert data["degree_checks"][0]["exact_sufficiency_ratio"].numerator // data["degree_checks"][0]["exact_sufficiency_ratio"].denominator == 1776281


def test_shared_matches_cannot_be_treated_as_independent():
    mean, second = exact_uniform_moments(3)
    count, one_probability = 16, F(1, 16)
    false_independent_second = mean*mean+count*one_probability*(1-one_probability)
    assert mean == 1
    assert second > false_independent_second


@pytest.mark.parametrize("rank", [3, 4, 5, 6, 7, 8, 9])
def test_sorted_join_matches_exhaustive_filtered_search(rank):
    rng = random.Random(26027+rank)
    length = 2**((rank+2)//3)
    lists = [[rng.randrange(2**rank) for _ in range(length)] for _ in range(4)]
    target = rng.randrange(2**rank)
    mask = (1 << (rank//3))-1
    expected = any((a ^ b ^ c ^ d) == target and not ((a ^ b) & mask)
                   for a, b, c, d in product(*lists))
    result = four_list_match(lists, rank, target)
    assert (result["indices"] is not None) == expected
    assert not result["hardness_evidence"]
    if expected:
        labels = result["labels"]
        assert labels[0] ^ labels[1] ^ labels[2] ^ labels[3] == target
        assert not result["native_relation_verified"]


def test_cap_is_unknown_not_infeasibility():
    result = four_list_match([[0, 0]]*4, 3, 0, pair_cap=1)
    assert result["status"] == "UNKNOWN_PAIR_CAP"
    assert result["indices"] is None and not result["hardness_evidence"]


def test_bad_distribution_has_no_implicit_success_guarantee():
    result = four_list_match([[0, 0]]*4, 3, 1)
    assert result["status"] == "UNKNOWN_NO_FILTERED_MATCH"
    assert not overlap_certificate()["distribution_premise_verified_by_this_certificate"]


@pytest.mark.parametrize("e", [0, 7, 9, True])
def test_no_invented_tower_levels(e):
    with pytest.raises(ValueError):
        tower_certificate(e)


def test_binary_rank_against_exhaustive_span():
    for vectors in product(range(8), repeat=3):
        values = {0}
        for vector in vectors:
            values |= {value ^ vector for value in values}
        assert len(values) == 2**binary_rank(vectors)


@pytest.mark.parametrize("rank", [3, 4, 5, 6, 7, 8, 9])
def test_independent_uniform_mixture_calculation_matches_rank_formula(rank):
    assert exact_mixture_moments(rank, 2**rank-1, [0]*4, [0]*4) == exact_uniform_moments(rank)


@pytest.mark.parametrize("rank,target,atoms", [
    (3, 0, [0, 0, 0, 0]),
    (3, 7, [1, 2, 4, 7]),
    (4, 11, [1, 3, 7, 15]),
    (5, 21, [3, 9, 16, 31]),
    (6, 63, [1, 19, 42, 54]),
])
def test_exact_biased_moments_survive_target_and_nonidentical_laws(rank, target, atoms):
    length = 2**((rank+2)//3)
    alpha = F(1, 4*length)
    strengths = [alpha, alpha/2, alpha/3, alpha]
    mean, second = exact_mixture_moments(rank, target, atoms, strengths)
    assert mean >= F(7, 8)
    assert second <= F(117, 16)**4
    assert mean*mean/second > F(1, 4000)


def test_conditioned_affine_system_matches_direct_single_tuple_sum():
    rank, target, atoms = 3, 7, [0, 1, 3, 4]
    strengths = [F(1, 8), F(1, 16), F(1, 24), F(1, 8)]
    laws = [[(1-a)/8+a*(x == atom) for x in range(8)] for atom, a in zip(atoms, strengths)]
    direct = F(0)
    for a, b, c, d in product(range(8), repeat=4):
        if not ((a ^ b) & 1) and a ^ b ^ c ^ d == target:
            direct += laws[0][a]*laws[1][b]*laws[2][c]*laws[3][d]
    assert mixture_joint_probability(rank, target, atoms, strengths, 15) == direct
    assert mixture_joint_probability(rank, target, atoms, strengths, 0) == direct*direct


def test_outside_bias_contract_can_have_zero_success():
    assert exact_mixture_moments(3, 1, [0]*4, [1]*4) == (0, 0)
