from fractions import Fraction
from itertools import product
import random

import pytest

from exact_control import fixture
from norm_sampling import NormCompletion, RankWeightedNormSampler, ag_sampling_bounds
from norm_completion import rank


class ScriptedRandom:
    def __init__(self, values):
        self.values = iter(values)

    def randrange(self, *args):
        value = next(self.values)
        assert value in range(*args)
        return value


def unequal_rank_case():
    return NormCompletion(5, [[1, 4, 0, 0], [0, 0, 1, 4]],
                          [[1, 1, 0, 0], [0, 0, 1, 1]], [1]*4, 2)


@pytest.mark.parametrize("R", [0, 1])
def test_exact_incidence_density_with_unequal_restriction_ranks(R):
    case = unequal_rank_case()
    p, k, r, t = case.p, case.k, case.r, len(case.T)
    denominator = p**(2*R)+p**k-1
    Z = Fraction(denominator, p**(2*R))
    cosets = p**(2*t-2*r)
    combinations, ranks = [], set()
    for coefficient in product(range(p), repeat=k):
        if not any(coefficient):
            continue
        c = [sum(coefficient[j]*case.B[j][i] for j in range(k)) % p for i in case.T]
        U = [[row[i]*case.h[i]*v % p for i, v in zip(case.T, c)] for row in case.A]
        rank_u = rank(U, p)
        ranks.add(rank_u)
        combinations.append((U, rank_u))
    assert ranks == {1, 2}
    wrong_ratios = set()
    for tail in product(range(p), repeat=4):
        a, b = [0, tail[0], 0, tail[1]], [0, tail[2], 0, tail[3]]
        M = case.prepare([0, 1], a, b)["matrix"]
        d = k-rank(M, p)
        mass = Fraction(p**(2*R), denominator*cosets)
        wrong = mass
        for U, rank_u in combinations:
            if any(sum(x*y for x, y in zip(row, vector)) % p for row in U for vector in (a, b)):
                continue
            conditional_cosets = p**(2*(t-rank_u-r))
            component = Fraction(1, denominator*conditional_cosets)
            mass += component*Fraction(1, p**(2*(rank_u-R)))
            wrong += component
        assert mass == Fraction(p**d, cosets)/Z
        wrong_ratios.add(wrong/Fraction(p**d, cosets))
    assert len(wrong_ratios) > 1  # Omitting thinning is not a constant rescaling.


def test_incident_offset_is_sampled_in_actual_kernel():
    case = fixture()
    sampler = RankWeightedNormSampler(case, 2)
    # Incident branch, lambda1, thinning coin0, then two nullspace vectors.
    proposal = sampler.offset_proposal(ScriptedRandom([625, 1, 0, 1, 2, 3, 4]))
    assert proposal["branch"] == "INCIDENT"
    assert proposal["restriction_rank"] == 2
    M = case.prepare([1], proposal["a"], proposal["b"])["matrix"]
    assert all(x == 0 for x in M[0])


def test_thinning_rejects_instead_of_looping():
    sampler = RankWeightedNormSampler(fixture(), 1)
    result = sampler.offset_proposal(ScriptedRandom([25, 1, 1]))
    assert result["status"] == "REJECT_THINNING"


def test_observed_violation_of_rank_promise_fails_closed():
    sampler = RankWeightedNormSampler(unequal_rank_case(), 2)
    with pytest.raises(ValueError, match="promise contradicted"):
        sampler.offset_proposal(ScriptedRandom([625, 1]))


def test_rank_deficient_reachable_coset_is_not_discarded(monkeypatch):
    case = fixture()
    sampler = RankWeightedNormSampler(case, 0)
    monkeypatch.setattr(sampler, "offset_proposal", lambda rng: {"branch": "INCIDENT", "a": [0]*4, "b": [0]*4})
    result = sampler.one_trial([1], ScriptedRandom([1, 1, 0, 0, 0]))
    assert result["status"] == "VERIFIED_NATIVE_WITNESS"
    assert result["syndrome_rank"] == 0 and result["kernel_dimension"] == 4
    assert case.verifies(result["word"], [1])


def test_rank_deficient_unreachable_target_rejects_whole_trial(monkeypatch):
    sampler = RankWeightedNormSampler(fixture(), 0)
    monkeypatch.setattr(sampler, "offset_proposal", lambda rng: {"branch": "INCIDENT", "a": [0]*4, "b": [0]*4})
    result = sampler.one_trial([1], ScriptedRandom([2]))
    assert result["status"] == "REJECT_INCONSISTENT_TARGET"


@pytest.mark.parametrize("R", [0, 1, 2])
def test_exact_sampler_native_relation_and_declared_promise(R):
    case = fixture()
    sampler = RankWeightedNormSampler(case, R)
    for s in range(5):
        result = sampler.draw([s], seed=27150+s)
        assert result["status"] == "VERIFIED_NATIVE_WITNESS"
        assert case.verifies(result["word"], [s])
        assert result["exact_uniform_given_rank_promise"]
        assert result["universal_rank_promise_checked"] == (R == 0)
        assert result["exact_uniform_native_claim"] == (R == 0)


def test_every_small_fixture_nonzero_lambda_meets_rank_promise():
    case = fixture()
    for coefficient in range(1, 5):
        U = [[row[i]*case.h[i]*coefficient*case.B[0][i] % 5 for i in case.T] for row in case.A]
        assert rank(U, 5) == 2


def test_exact_sampling_success_bound():
    bounds = ag_sampling_bounds(1019, 64)
    assert bounds["rank_weighted_trial_success_lower"] > Fraction(99, 100)
    assert bounds["rank_weighted_trial_success_lower"] < bounds["trial_success_lower"]


def test_large_integer_coins_have_polynomial_bit_descriptions():
    p, k, R = 1019, 323, 165
    assert (p**(2*R)+p**k-1).bit_length() <= (max(2*R, k)+1)*p.bit_length()


def test_invalid_rank_promises_rejected():
    for bad in (-1, 3, True, 0.5):
        with pytest.raises(ValueError):
            RankWeightedNormSampler(fixture(), bad)
