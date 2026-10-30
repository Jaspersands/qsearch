from fractions import Fraction as F
from itertools import product
from math import prod, sqrt

import pytest

from copy_boundary import (
    StripeFamily, birthday_upper, canonical_purification_gap,
    ceil_sqrt_rational, classical_moments, classical_sufficient_copies,
    collision_probability, collision_score, exhaustive_control,
    hoeffding_exponent, mixture_chi_squared, necessary_copies,
    sqrt_interval, tv_squared_upper,
)


@pytest.mark.parametrize("p", [2, 3, 5])
@pytest.mark.parametrize("v", [F(1, 5), F(3, 4), F(1)])
def test_direct_states_have_same_spectrum_but_different_conjugation_stabilizers(p, v):
    family = StripeFamily(2, v, p)
    theta = (0, p - 1)
    null = family.distribution(theta, "null")
    signal = family.distribution(theta, "signal")
    metrics = family.metrics()
    assert sum(null.values()) == sum(signal.values()) == 1
    assert sorted(null.values()) == sorted(signal.values())
    assert sum(x > 0 for x in null.values()) == metrics["rank"]
    assert sum(x*x for x in null.values()) == metrics["purity_both_cases"]
    for shift in range(1, p):
        shifted = {(b, a, r): signal[b, a, (r-shift) % p] for b, a, r in signal}
        assert all(null[b, a, r] == null[b, a, (r-shift) % p] for b, a, r in null)
        assert sum(abs(signal[x]-shifted[x]) for x in signal)/2 == v
        cross = sum(signal[x]*shifted[x] for x in signal)
        assert cross / sum(x*x for x in signal.values()) == metrics["signal_normalized_hs_overlap"]
        assert sum((signal[x]-shifted[x])**2 for x in signal) == metrics["signal_absolute_hs_distance_squared"]
        # Trace(diagonal(rho) * permutation) only sees fixed basis points.
        assert sum(signal[x] for x in signal if (x[2]+shift) % p == x[2]) == 0
        assert sum(null[x] for x in null if (x[2]+shift) % p == x[2]) == 0
        if v == 1:
            assert cross == 0


@pytest.mark.parametrize("p,m,t", [(2, 1, 0), (2, 1, 3), (3, 2, 1), (3, 2, 2), (3, 2, 3)])
@pytest.mark.parametrize("v", [F(1, 2), F(1)])
def test_exhaustive_joint_states_match_all_bounds(p, m, t, v):
    result = exhaustive_control(StripeFamily(m, v, p), t)
    if t <= 1:
        assert result["tv"] == 0
    if t == 2:
        assert result["tv"] == v**2 * F(p-1, p*m)
        assert result["chi_squared_each_vs_uniform"] == F(p-1, m)*v**4


@pytest.mark.parametrize("case", ["null", "signal"])
@pytest.mark.parametrize("v", [F(3, 4), F(1)])
def test_count_likelihood_against_independent_hidden_orientation_enumeration(case, v):
    family = StripeFamily(2, v)
    words = [(), ((0, 0, 0),), ((0, 0, 0), (1, 1, 2)),
             ((0, 0, 0), (0, 0, 1)), ((0, 0, 0), (0, 1, 0), (1, 2, 1)),
             ((0, 0, 0),)*4]
    for samples in words:
        direct = family.direct_mixture_probability(samples, case)
        assert direct == family.mixture_likelihood(samples, case)/family.dimension**len(samples)


def test_fixed_orientation_is_not_fresh_randomization_each_copy():
    family = StripeFamily(2)
    samples = ((0, 0, 0), (0, 0, 1))
    fixed_null = family.direct_mixture_probability(samples, "null")
    fixed_signal = family.direct_mixture_probability(samples, "signal")
    fresh = prod(family.direct_mixture_probability((x,), "null") for x in samples)
    assert fixed_null > fresh > fixed_signal
    assert fresh == F(1, family.dimension**2)


@pytest.mark.parametrize("case", ["null", "signal"])
def test_no_collision_laws_agree_exactly(case):
    family = StripeFamily(3, F(5, 7))
    for coordinates in product(range(3), repeat=6):
        samples = tuple((b, coordinates[2*b], coordinates[2*b+1]) for b in range(3))
        assert family.mixture_likelihood(samples, case) == 1


@pytest.mark.parametrize("p,m,v,t", [(2, 1, F(1, 2), 3), (3, 2, F(3, 4), 3), (3, 1, F(1), 4)])
def test_classical_score_moments_against_direct_fixed_state_enumeration(p, m, v, t):
    family = StripeFamily(m, v, p)
    expected = classical_moments(family, t)
    for case in ("null", "signal"):
        distribution = family.distribution(tuple(b % p for b in range(m)), case)
        mean = second = F(0)
        for samples in product(distribution, repeat=t):
            probability = prod(distribution[x] for x in samples)
            score = collision_score(samples)
            # Independent pairwise implementation checks the hash-count score.
            pair_score = sum(int(samples[i][0] == samples[j][0]) *
                             (int(samples[i][1] == samples[j][1])-
                              int(samples[i][2] == samples[j][2]))
                             for i in range(t) for j in range(i+1, t))
            assert score == pair_score
            mean += probability*score
            second += probability*score**2
        assert mean == expected[f"{case}_mean"]
        assert second-mean**2 == expected["variance_both_cases"]


@pytest.mark.parametrize("m", [1, 2, 17, 2**64])
@pytest.mark.parametrize("v", [F(1, 100), F(3, 4), F(1)])
def test_analytic_classical_budget_and_quantum_lower_bound(m, v):
    family = StripeFamily(m, v)
    copies = classical_sufficient_copies(family)
    assert classical_moments(family, copies)["error_upper_chebyshev"] < F(1, 3)
    bounds = necessary_copies(family)
    birthday = bounds["birthday_necessary_copies"]
    assert birthday*(birthday-1) >= F(2*m, 3)
    assert (birthday-1)*(birthday-2) < F(2*m, 3)
    chi = bounds["rational_chi_necessary_copies"]
    rhs = F(16*m, 11*family.order**2)/v**4
    assert chi**2 >= rhs > (chi-1)**2
    assert bounds["combined_necessary_copies"] <= copies
    assert tv_squared_upper(family, bounds["combined_necessary_copies"]-1) < F(1, 9)


@pytest.mark.parametrize("p,v", [(2, F(1, 10)), (3, F(3, 4)), (3, F(1)), (5, F(4, 5))])
def test_canonical_purification_has_constant_nontrivial_character_probability(p, v):
    family = StripeFamily(2, v, p)
    null = family.distribution((0, 1), "null")
    signal = family.distribution((0, 1), "signal")
    overlap = sum(sqrt(float(signal[b,a,r]*signal[b,a,(r+1) % p])) for b,a,r in signal)
    null_overlap = sum(sqrt(float(null[b,a,r]*null[b,a,(r+1) % p])) for b,a,r in null)
    gap = (p-1)*(1-overlap)/p
    low, high = canonical_purification_gap(family)
    assert 0 < low <= high < 1
    assert abs(gap-float(low)) < 1e-14
    assert abs(null_overlap-1) < 1e-14
    assert canonical_purification_gap(StripeFamily(2**64, v, p)) == (low, high)


def test_rank_gap_and_purity_normalization_are_not_silently_changed():
    small, large = StripeFamily(1).metrics(), StripeFamily(2**64).metrics()
    for name in ("signal_trace_distance_nonidentity", "signal_normalized_hs_overlap"):
        assert small[name] == large[name]
    assert small["signal_absolute_hs_distance_squared"] == 2**64 * large["signal_absolute_hs_distance_squared"]
    assert large["rank"] == large["dimension"]
    assert StripeFamily(2**64, F(1)).metrics()["rank"] == 3*2**64


def test_large_certificate_does_not_enumerate_states():
    family = StripeFamily(2**128, F(3, 4))
    assert tv_squared_upper(family, 10**6) < F(1, 10**20)
    assert necessary_copies(family)["combined_necessary_copies"] > 10**19
    assert hoeffding_exponent(family, 10**30) > 1
    assert tv_squared_upper(family, 10**30) == 1
    with pytest.raises(ValueError):
        family.alphabet()
    with pytest.raises(ValueError):
        exhaustive_control(family, 2)
    with pytest.raises(ValueError):
        mixture_chi_squared(family, 2)


@pytest.mark.parametrize("value", [F(0), F(1), F(2), F(3, 7), F(10**100, 3)])
def test_exact_square_root_bounds(value):
    low, high = sqrt_interval(value)
    assert low**2 <= value <= high**2
    assert high-low <= F(1, 2**64)
    ceil = ceil_sqrt_rational(value)
    assert ceil**2 >= value
    if ceil:
        assert (ceil-1)**2 < value


def test_collision_bounds_and_empty_samples():
    assert collision_probability(100, 0) == collision_probability(100, 1) == 0
    assert collision_probability(100, 2) == F(1, 100)
    assert collision_probability(3, 4) == 1
    assert birthday_upper(3, 4) == 1
    assert collision_score(()) == 0
    with pytest.raises(ValueError):
        collision_probability(10**9, 10001)


@pytest.mark.parametrize("kwargs", [{"buckets": 0}, {"buckets": True},
                                    {"buckets": 1, "order": 1},
                                    {"buckets": 1, "visibility": F(0)},
                                    {"buckets": 1, "visibility": F(5, 4)},
                                    {"buckets": 1, "visibility": 0.5}])
def test_invalid_family_contracts_fail_closed(kwargs):
    with pytest.raises(ValueError):
        StripeFamily(**kwargs)


def test_invalid_record_inputs_and_diagnostic_caps():
    family = StripeFamily(2)
    for case in ("unknown", ""):
        with pytest.raises(ValueError):
            family.mixture_likelihood((), case)
    for samples in [((2, 0, 0),), ((0, 3, 0),), ((0, 0),), ((False, 0, 0),)]:
        with pytest.raises(ValueError):
            family.mixture_likelihood(samples, "null")
    for theta in [(0,), (0, 3)]:
        with pytest.raises(ValueError):
            family.distribution(theta, "null")
    with pytest.raises(ValueError):
        necessary_copies(family, F(1, 2))
    with pytest.raises(ValueError):
        birthday_upper(2, -1)
    with pytest.raises(ValueError):
        classical_moments(family, 1)
    with pytest.raises(ValueError):
        StripeFamily(20).direct_mixture_probability((), "null")
