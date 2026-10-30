from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import ceil, comb

import pytest

from affine_sampling import AffineFiber, bonferroni_bound
from curve_countercontrol import control


def test_all_small_fibers_and_joint_marginals_are_uniform():
    fiber = AffineFiber(3, [[1]*7], relation="full_support")
    bound = bonferroni_bound(7, 3, 6)
    assert bound["success_lower"] > 0
    for syndrome in ((0,), (1,), (2,)):
        start = fiber.particular(syndrome)
        words = [tuple(fiber.fiber_word(start, c)) for c in product(range(3), repeat=6)]
        assert len(set(words)) == 729
        assert all(sum(word) % 3 == syndrome[0] for word in words)
        good = [word for word in words if all(word)]
        assert len(good) == (42 if syndrome == (0,) else 43)
        assert Fraction(len(good), len(words)) >= bound["success_lower"]
        for subset in combinations(range(7), 5):
            marginals = Counter(tuple(word[j] for j in subset) for word in words)
            assert len(marginals) == 3**5
            assert set(marginals.values()) == {3}


def test_false_independence_assumption_is_not_silently_certified():
    fiber = AffineFiber(3, [[1, 0, 0]], relation="full_support")
    bound = bonferroni_bound(3, 3, 3)
    assert bound["success_lower"] > 0
    assert not bound["independence_verified_by_this_helper"]
    assert fiber.sample((0,), seed=0, attempts=16)["status"] == "UNKNOWN_ATTEMPT_CAP"


def test_smooth_ag_gap_control_has_actual_classical_witnesses():
    fiber, data = control()
    assert data["prime"] < fiber.m
    assert data["cube_annihilator_dimension"] == 0
    assert data["refined_decoder_failure_upper"] < Fraction(1, 30)
    assert data["classical_probability_certificate"]["success_lower"] > Fraction(1, 5)
    assert data["128_trial_failure_below_1e_minus_12"]
    for index in range(32):
        syndrome = tuple((index**(j+1)+j) % fiber.p for j in range(fiber.k))
        result = fiber.sample(syndrome, seed=26000+index, attempts=128)
        assert result["status"] == "VERIFIED_FULL_SUPPORT_WITNESS"
        assert fiber.verifies(result["witness"], syndrome)
        assert result["field_draws"] == result["attempts"]*14


def test_explicit_zero_and_basis_syndromes_in_same_gap_control():
    fiber, _ = control()
    for i, syndrome in enumerate([(0,)*fiber.k]+[tuple(int(i == j) for j in range(fiber.k))
                                                for i in range(fiber.k)]):
        result = fiber.sample(syndrome, seed=27000+i)
        assert fiber.verifies(result["witness"], syndrome)


def test_classical_bound_is_not_inferred_from_quantum_success():
    # Fixed small field, large mean zero count: no fake polynomial certificate.
    bound = bonferroni_bound(1000, 13, 11)
    assert bound["success_lower"] == 0
    assert bound["expected_trials_upper"] is None


@pytest.mark.parametrize("length,prime", [(100, 31), (200, 101), (1000, 101)])
def test_exact_analytic_remainder_and_half_product_bound(length, prime):
    mu = Fraction(length, prime)
    even_order = 2*ceil(4*(mu+1))
    assert even_order <= length//2
    bound = bonferroni_bound(length, prime, even_order-1)["success_lower"]
    independent = Fraction(prime-1, prime)**length
    remainder = Fraction(comb(length, even_order), prime**even_order)
    assert 0 <= independent-bound <= remainder
    assert bound >= independent/2


def test_finite_cap_preserves_conditional_uniformity_under_ideal_coins():
    fiber = AffineFiber(3, [[1, 1]], relation="full_support")
    start = fiber.particular((0,))
    outputs = Counter()
    failures = 0
    for first, second in product(range(3), repeat=2):
        for coefficient in (first, second):
            word = tuple(fiber.fiber_word(start, (coefficient,)))
            if all(word):
                outputs[word] += 1
                break
        else:
            failures += 1
    assert outputs == {(1, 2): 4, (2, 1): 4}
    assert failures == 1


def test_original_basis_with_noninitial_pivot_columns():
    B = [[0, 0, 1, 2], [0, 1, 1, 0]]
    fiber = AffineFiber(5, B, relation="full_support")
    assert fiber.pivots == [1, 2]
    start = fiber.particular((1, 4))
    words = {tuple(fiber.fiber_word(start, c)) for c in product(range(5), repeat=2)}
    assert len(words) == 25
    assert all(sum(row[j]*word[j] for j in range(4)) % 5 == target
               for word in words for row, target in zip(B, (1, 4)))


@pytest.mark.parametrize("args", [(0, 3, 0), (3, 1, 1), (3, 3, -1), (3, 3, 4),
                                  (True, 3, 1), (3, 3, True)])
def test_moment_bound_input_guards(args):
    with pytest.raises(ValueError):
        bonferroni_bound(*args)


def test_no_independence_means_no_positive_certificate():
    assert bonferroni_bound(3, 3, 0)["success_lower"] == 0


@pytest.mark.parametrize("prime", [2, 9, True, 3.0])
def test_prime_backend_guards(prime):
    with pytest.raises(ValueError):
        AffineFiber(prime, [[1, 1]], relation="full_support")


@pytest.mark.parametrize("data", [[], [[]], [[0, 0]], [[1], [2]], [[1], [1, 2]],
                                  [[True, 1]], [[1, 3]]])
def test_matrix_guards(data):
    with pytest.raises(ValueError):
        AffineFiber(3, data, relation="full_support")


def test_predicate_caps_and_original_equation_guards():
    with pytest.raises(ValueError):
        AffineFiber(3, [[1, 1]], relation="inverse_trace")
    fiber = AffineFiber(3, [[1, 1]], relation="full_support")
    for syndrome in ((3,), (True,), (), (1, 2)):
        with pytest.raises(ValueError):
            fiber.sample(syndrome, seed=0)
    for cap in (0, -1, True, 1.5):
        with pytest.raises(ValueError):
            fiber.sample((0,), seed=0, attempts=cap)
    assert not fiber.verifies((1, 1), (0,))
    result = fiber.sample((0,), seed=1, attempts=1)
    assert result["status"] == "UNKNOWN_ATTEMPT_CAP"
    assert result["field_draws"] == 1
    assert result["hardness_evidence"] is False
