from fractions import Fraction
from itertools import product
import random

import pytest

from exact_control import enumerate_control, fixture
from norm_sampling import GlobalNormSampler, ag_sampling_bounds, systematic_draw, weighted_bounds


@pytest.fixture(scope="module")
def exact():
    return enumerate_control()


def test_all_native_witnesses_have_equal_norm_multiplicity(exact):
    assert exact["norm_lift_multiplicities"] == [6**4]
    assert exact["native_reference_uniform"]
    case = fixture()
    expected = sum(sum(a*b for a, b in zip(case.B[0], word)) % 5 == 1
                   for word in product(range(1, 5), repeat=5))
    assert exact["native_witnesses"] == expected


def test_weighted_bad_coset_count_not_naive_conditioning(exact):
    assert exact["cosets"] == 625 and exact["good_cosets"] == 528
    assert exact["deficiency_moment"] == Fraction(4, 625)
    assert exact["weighted_bad_coset_mass"] == Fraction(101, 625)
    assert exact["weighted_bound_equals_probability_plus_moment"]
    assert exact["native_tv_exact"] <= exact["lift_tv_exact"] <= exact["native_tv_certified_upper"]


def test_rank_weighting_exactly_restores_original_uniform_law(exact):
    assert exact["rank_weighted_native_tv_exact"] == 0
    assert exact["rank_weighted_trial_success_exact"] > Fraction(4, 5)
    assert exact["discard_rank_deficient_native_tv_exact"] > 0
    assert exact["count_recovered_from_acceptance"] == exact["native_witnesses"]


def test_countercontrol_reusing_coset_biases_output(exact):
    assert exact["good_coset_valid_lift_min"] >= 125*(1-Fraction(4, 25))
    assert exact["good_coset_valid_lift_min"] < exact["good_coset_valid_lift_max"]
    assert exact["retry_same_coset_changes_law_tv"] > 0


def test_countercontrol_freezing_outside_restricts_native_law(exact):
    assert exact["freeze_outside_changes_law_tv"] > Fraction(1, 2)


def test_independent_trial_cap_does_not_change_conditional_law(exact):
    probability = exact["whole_trial_success_exact"]
    # Each accepted atom's mass is multiplied by this same geometric sum.
    for cap in (1, 2, 5, 16):
        clock = sum((1-probability)**j for j in range(cap))
        assert probability*clock == 1-(1-probability)**cap


def test_matrix_and_admission_are_coset_and_syndrome_invariant():
    case = fixture()
    sampler = GlobalNormSampler(case)
    rng = random.Random(27121)
    for _ in range(20):
        a, b = ([rng.randrange(5) for _ in case.T] for _ in range(2))
        shift = [rng.randrange(5) for _ in range(4)]
        a2 = [(a[j]+sum(shift[t]*case.A[t][i] for t in range(2))) % 5
              for j, i in enumerate(case.T)]
        b2 = [(b[j]+sum(shift[2+t]*case.A[t][i] for t in range(2))) % 5
              for j, i in enumerate(case.T)]
        first = case.prepare([0], a, b)
        second = case.prepare([4], a2, b2)
        assert first["matrix"] == second["matrix"]
        for s in range(5):
            for value in range(1, 5):
                admitted = sampler.prepare([s], [value], a, b)
                reference = sampler.prepare([0], [1], a2, b2)
                assert admitted["status"] == reference["status"]


def test_single_trial_draws_outside_offsets_and_kernel_once(monkeypatch):
    case = fixture()
    sampler = GlobalNormSampler(case)
    calls = []
    actual = case.sample
    def counted(prepared, rng):
        calls.append(prepared["point"])
        return actual(prepared, rng)
    monkeypatch.setattr(case, "sample", counted)
    rng = random.Random(27122)
    outside = set()
    for _ in range(80):
        before = len(calls)
        result = sampler.one_trial([1], rng)
        assert len(calls)-before <= 1
        if result["word"]:
            assert case.verifies(result["word"], [1])
            outside.add(result["word"][-1])
    assert outside == {1, 2, 3, 4}


def test_rejection_restarts_entire_trial(monkeypatch):
    sampler = GlobalNormSampler(fixture())
    calls = []
    def trial(syndrome, rng):
        calls.append(rng.randrange(5))
        return {"status": "REJECT_ZERO_NORM", "word": None}
    monkeypatch.setattr(sampler, "one_trial", trial)
    result = sampler.draw([1], seed=1, attempts=3)
    assert len(calls) == 3
    assert result["status"] == "UNKNOWN_ATTEMPT_CAP"
    assert not result["hardness_evidence"]


@pytest.mark.parametrize("s", range(5))
def test_original_relation_and_honest_sampling_status(s):
    case = fixture()
    result = GlobalNormSampler(case).draw([s], seed=27123+s)
    assert result["status"] == "VERIFIED_NATIVE_WITNESS"
    assert case.verifies(result["word"], [s])
    assert result["distribution"] == "GOOD_COSET_NORM_PUSHFORWARD"
    assert not result["exact_uniform_native_claim"]
    assert not result["universal_rank_promise_checked"]


def test_syndrome_iterator_is_consumed_once():
    case = fixture()
    result = GlobalNormSampler(case).draw(iter([1]), seed=27123)
    assert case.verifies(result["word"], [1])


@pytest.mark.parametrize("e", [8, 16, 32, 63])
def test_small_e_exact_systematic_bound(e):
    bound = ag_sampling_bounds(1019, e)
    assert bound["tv_upper"] == 0
    assert bound["trial_success_lower"] > Fraction(1, 2)


@pytest.mark.parametrize("e", [64, 65, 67, 69, 128, 256, 16384, 23599])
def test_ag_statistical_bound(e):
    bound = ag_sampling_bounds(1019, e)
    assert bound["useful_certificate"]
    assert bound["constant_success_scope"]
    assert bound["trial_success_lower"] > Fraction(1, 4)
    assert bound["tv_upper"] < Fraction(1, 10**11)
    assert not bound["rank_promise_checked_by_this_function"]


def test_no_fixed_prime_asymptotic_claim():
    bound = ag_sampling_bounds(1019, 1019**2)
    assert not bound["constant_success_scope"]
    assert not bound["useful_certificate"]
    assert bound["trial_success_lower"] == 0
    assert bound["tv_upper"] == 1


def test_systematic_sampler_original_relation():
    case = fixture()
    for s in range(5):
        result = systematic_draw(5, case.B, [s], seed=27124+s)
        assert case.verifies(result["word"], [s])
        assert result["exact_uniform_conditional_on_success"]
        assert not result["efficiency_promise_checked"]


def test_systematic_full_enumeration_bijection():
    case = fixture()
    inverse = pow(case.B[0][0], -1, 5)
    for s in range(5):
        observed = []
        for free in product(range(1, 5), repeat=4):
            first = (s-sum(a*b for a, b in zip(case.B[0][1:], free)))*inverse % 5
            if first:
                observed.append((first, *free))
        expected = {word for word in product(range(1, 5), repeat=5)
                    if sum(a*b for a, b in zip(case.B[0], word)) % 5 == s}
        assert len(observed) == len(set(observed))
        assert set(observed) == expected


def test_invalid_inputs_are_rejected():
    sampler = GlobalNormSampler(fixture())
    with pytest.raises(ValueError):
        sampler.prepare([1], [0], [0]*4, [0]*4)
    with pytest.raises(ValueError):
        sampler.draw([1], seed=0, attempts=0)
    with pytest.raises(ValueError):
        sampler.draw([5], seed=0)
    with pytest.raises(ValueError):
        weighted_bounds(5, 1, 4, 0)
    with pytest.raises(ValueError):
        ag_sampling_bounds(1019, 7)
    with pytest.raises(ValueError):
        systematic_draw(5, [[1, 1], [1, 1]], [0, 0], seed=0)
