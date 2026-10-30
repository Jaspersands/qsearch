"""Exact finite controls and oracle-relative sampler contract regressions.

Scripted RNGs test branch boundaries, not iid randomness. Mock Walsh oracles
exercise the interface only and do not establish native Walsh access.
"""
from collections import Counter, deque
from decimal import Decimal
from fractions import Fraction
from math import ceil, isqrt

import pytest

from theorems import balanced_signed_mpi
from theorems import mersenne_reciprocal_access as access
from theorems import mersenne_reciprocal_curve as curve


NATIVE_BITS, NATIVE_S = 17, 3
NATIVE_Q = 1 << NATIVE_BITS
CANONICAL_PRIMES = [
    n for n in range(17, 128)
    if all(n % divisor for divisor in range(2, isqrt(n)+1))
]


class ScriptedRng:
    def __init__(self, draws):
        self.draws = deque(draws)
        self.stops = []

    def randrange(self, stop):
        expected_stop, value = self.draws.popleft()
        assert stop == expected_stop
        self.stops.append(stop)
        return value

    def assert_exhausted(self):
        assert not self.draws


@pytest.fixture(scope="module")
def native_spectrum():
    return access.finite_walsh_spectrum(NATIVE_BITS, NATIVE_S)


@pytest.fixture(scope="module")
def native_differential():
    # Enumerate the native vector map, not the Frobenius-relabeled rank helper.
    vector = [curve.reciprocal_value(NATIVE_BITS, NATIVE_S, x)
              for x in range(NATIVE_Q)]
    return Counter(vector[x ^ 1] ^ vector[x] for x in range(NATIVE_Q))


def native_oracle(spectrum, calls):
    def oracle(bits, s, frequency):
        assert (bits, s) == (NATIVE_BITS, NATIVE_S)
        calls.append(frequency)
        return spectrum[frequency]

    return oracle


def exact_clipped_law(spectrum, threshold):
    q = len(spectrum)
    target = tuple(Fraction(value*value, q*q) for value in spectrum)
    clipped = tuple(min(probability, Fraction(threshold, q))
                    for probability in target)
    mass = sum(clipped, Fraction(0))
    law = tuple(probability/mass for probability in clipped)
    tv = sum((abs(p-r) for p, r in zip(target, law)), Fraction(0))/2
    return target, law, mass, tv


@pytest.mark.parametrize("bits", CANONICAL_PRIMES)
def test_differential_bound_covers_every_canonical_prime(bits):
    s = (bits-3)//4
    remainder = bits-4*s
    assert remainder in (3, 5)
    bound = access.differential_uniformity_bound(bits)
    assert type(bound) is int
    assert bound == {3: 14, 5: 30}[remainder]


@pytest.mark.parametrize("bits", [17, 19, 61, 127])
@pytest.mark.parametrize("epsilon,abort_bits", [
    (Fraction(1, 8), 16), (Fraction(1, 2), 1),
    (Fraction(2, 7), 3), (Fraction(1, 257), 37),
    (Fraction(1, (1 << 60)+1), 5),
])
def test_budget_is_exact_including_both_ceiling_operations(bits, epsilon, abort_bits):
    budget = access.clipped_sampler_budget(bits, epsilon, abort_bits)
    s = (bits-3)//4
    delta = {3: 14, 5: 30}[bits-4*s]
    threshold = ceil(Fraction(delta)/epsilon)
    expected = Fraction(threshold)/(1-epsilon)
    abort = Fraction(1, 1 << abort_bits)
    assert budget["bits"] == bits and budget["s"] == s
    assert budget["differential_uniformity_upper"] == delta
    assert budget["clip_threshold"] == threshold
    assert type(budget["clip_threshold"]) is int
    assert budget["trial_cap"] == ceil(expected*abort_bits)
    assert type(budget["trial_cap"]) is int
    for key, value in {
        "expected_oracle_queries_upper": expected,
        "conditional_tv_upper": epsilon,
        "abort_probability_upper": abort,
        "unconditional_tv_upper": epsilon+abort,
    }.items():
        assert type(budget[key]) is Fraction
        assert budget[key] == value
    assert budget["walsh_oracle_required"] is True
    assert budget["polynomial_classical_walsh_access_established"] is False
    assert budget["oracle_correctness_assumed_not_verified"] is True
    assert budget["independent_uniform_randomness_required"] is True
    assert budget["field_tables_materialized"] is False
    assert "sampler overhead only" in budget["table_accounting_scope"]
    assert budget["external_oracle_time_accounted"] is False
    assert budget["external_oracle_space_accounted"] is False
    assert budget["polynomial_total_classical_runtime_established"] is False


def test_default_budget_and_nonvacuous_abort_bound():
    budget = access.clipped_sampler_budget(17)
    assert budget == access.clipped_sampler_budget(17, Fraction(1, 8), 16)
    assert budget["clip_threshold"] == 240
    assert budget["expected_oracle_queries_upper"] == Fraction(1920, 7)
    assert budget["trial_cap"] == 4389
    assert budget["unconditional_tv_upper"] == Fraction(8193, 65536)
    lower_acceptance = (1-budget["conditional_tv_upper"])/budget["clip_threshold"]
    assert (1-lower_acceptance)**budget["trial_cap"] <= budget["abort_probability_upper"]


def test_positive_abort_bits_has_no_undocumented_upper_bound():
    abort_bits = 1_000_001
    budget = access.clipped_sampler_budget(17, abort_bits=abort_bits)
    assert budget["abort_probability_upper"] == Fraction(1, 1 << abort_bits)
    assert budget["trial_cap"] == ceil(Fraction(1920, 7)*abort_bits)


def test_native_fourier_probability_and_vector_fourth_moment(native_spectrum,
                                                           native_differential):
    q = NATIVE_Q
    assert len(native_spectrum) == q and native_spectrum[0] == 0
    assert all(type(value) is int and value % 2 == 0 for value in native_spectrum)
    probabilities = tuple(Fraction(value*value, q*q) for value in native_spectrum)
    assert sum(probabilities, Fraction(0)) == 1
    differential_moment = sum(count*count for count in native_differential.values())
    fourth_moment = sum(value**4 for value in native_spectrum)
    assert sum(native_differential.values()) == q
    assert native_differential[0] == 0 and native_differential[1] == 2
    assert max(native_differential.values()) <= 30
    assert fourth_moment == q*q*differential_moment
    collision = sum((p*p for p in probabilities), Fraction(0))
    assert collision == Fraction(differential_moment, q*q)
    assert collision <= Fraction(30, q)


@pytest.mark.parametrize("bits,s", [(3, 1), (5, 2), (5, 4), (7, 2)])
def test_small_fields_exhaustive_differential_rows_and_fourth_moment(bits, s):
    q = 1 << bits
    vector = [curve.reciprocal_value(bits, s, x) for x in range(q)]
    assert len(set(vector)) == q
    row_moments = []
    for shift in range(1, q):
        row = Counter(vector[x ^ shift] ^ vector[x] for x in range(q))
        assert sum(row.values()) == q
        row_moments.append(sum(count*count for count in row.values()))
    assert len(set(row_moments)) == 1
    spectrum = access.finite_walsh_spectrum(bits, s)
    assert sum(value**4 for value in spectrum) == q*q*row_moments[0]


@pytest.mark.parametrize("threshold", [1, 4, 60, 240])
def test_exact_clipping_normalization_tv_and_acceptance(native_spectrum, threshold):
    target, law, mass, tv = exact_clipped_law(native_spectrum, threshold)
    assert sum(target, Fraction(0)) == sum(law, Fraction(0)) == 1
    assert law[0] == 0
    assert 0 < mass <= 1
    assert tv <= 1-mass <= Fraction(30, threshold)
    acceptance = sum((Fraction(min(w*w, threshold*NATIVE_Q), threshold*NATIVE_Q**2)
                      for w in native_spectrum), Fraction(0))
    assert acceptance == mass/threshold
    assert tuple(Fraction(min(w*w, threshold*NATIVE_Q), threshold*NATIVE_Q**2)/acceptance
                 for w in native_spectrum) == law
    if threshold in (1, 4):
        assert 0 < tv < 1-mass
    else:
        assert mass == 1 and tv == 0 and law == target


def test_finite_report_moments_and_clipping_use_cached_native_spectrum(
        native_spectrum, native_differential, monkeypatch):
    calls = []

    def cached_spectrum(bits, s):
        calls.append((bits, s))
        assert (bits, s) == (NATIVE_BITS, NATIVE_S)
        return native_spectrum

    monkeypatch.setattr(access, "finite_walsh_spectrum", cached_spectrum)
    report = access.finite_fourier_report(NATIVE_BITS, NATIVE_S)
    assert calls == [(NATIVE_BITS, NATIVE_S)]
    second = sum(count*count for count in native_differential.values())
    fourth = sum(value**4 for value in native_spectrum)
    assert report["differential_second_moment"] == second
    assert report["walsh_fourth_moment"] == fourth == NATIVE_Q**2*second
    assert report["fourth_moment_identity_checked"] is True
    assert report["differential_maximum_observed"] == max(native_differential.values())
    assert report["differential_count_histogram"] == dict(Counter(
        native_differential.get(c, 0) for c in range(NATIVE_Q)))
    assert report["canonical_differential_bound"] == 30
    assert report["canonical_differential_bound_checked"] is True
    assert report["collision_probability"] == Fraction(fourth, NATIVE_Q**4)
    assert type(report["collision_probability"]) is Fraction
    controls = report["finite_clipping_controls"]
    assert [row["clip_threshold"] for row in controls] == [1, 4, 240]
    for row in controls:
        threshold = row["clip_threshold"]
        _, _, mass, tv = exact_clipped_law(native_spectrum, threshold)
        for key, expected in {
            "lost_mass": 1-mass, "tv_from_target": tv,
            "acceptance_probability": mass/threshold,
            "expected_proposals": threshold/mass,
        }.items():
            assert type(row[key]) is Fraction
            assert row[key] == expected
        assert row["tv_bounded_by_lost_mass"] is True


def test_noncanonical_finite_report_does_not_claim_canonical_bound():
    report = access.finite_fourier_report(5, 4)
    assert report["fourth_moment_identity_checked"] is True
    assert report["differential_maximum_observed"] == 32
    assert report["walsh_fourth_moment"] == 32**4
    assert report["collision_probability"] == 1
    assert report["canonical_differential_bound"] is None
    assert report["canonical_differential_bound_checked"] is None
    assert [row["clip_threshold"] for row in report["finite_clipping_controls"]] == [1, 4]


def test_every_native_walsh_class_has_exact_integer_acceptance_boundary(native_spectrum):
    budget = access.clipped_sampler_budget(NATIVE_BITS)
    denominator = budget["clip_threshold"]*NATIVE_Q
    representatives = {value: a for a, value in enumerate(native_spectrum)}
    fallback = next(a for a, value in enumerate(native_spectrum) if value != 0)
    assert min(representatives) < 0 < max(representatives)
    assert 0 in representatives
    for value, frequency in representatives.items():
        accepted_draws = min(value*value, denominator)
        probes = {0, denominator-1}
        if accepted_draws:
            probes.add(accepted_draws-1)
        if accepted_draws < denominator:
            probes.add(accepted_draws)
        for draw in probes:
            accepted_first = draw < accepted_draws
            script = [(NATIVE_Q, frequency), (denominator, draw)]
            if not accepted_first:
                script += [(NATIVE_Q, fallback), (denominator, 0)]
            rng, calls = ScriptedRng(script), []
            result = access.sample_clipped_fourier(
                NATIVE_BITS, native_oracle(native_spectrum, calls), rng=rng)
            expected_frequency = frequency if accepted_first else fallback
            expected_queries = 1 if accepted_first else 2
            assert result == budget | {
                "status": "ACCEPTED", "frequency": expected_frequency,
                "oracle_queries": expected_queries,
            }
            assert calls == ([frequency] if accepted_first else [frequency, fallback])
            rng.assert_exhausted()


def test_cap_abort_and_acceptance_on_final_trial(native_spectrum):
    epsilon, abort_bits = Fraction(1, 2), 1
    budget = access.clipped_sampler_budget(NATIVE_BITS, epsilon, abort_bits)
    cap, denominator = budget["trial_cap"], budget["clip_threshold"]*NATIVE_Q
    fallback = next(a for a, value in enumerate(native_spectrum) if value != 0)
    for accept_last in (False, True):
        script = [(NATIVE_Q, 0), (denominator, 0)]*cap
        if accept_last:
            script[-2] = (NATIVE_Q, fallback)
        rng, calls = ScriptedRng(script), []
        result = access.sample_clipped_fourier(
            NATIVE_BITS, native_oracle(native_spectrum, calls), epsilon, abort_bits, rng)
        assert result == budget | {
            "status": "ACCEPTED" if accept_last else "ABORT",
            "frequency": fallback if accept_last else None, "oracle_queries": cap,
        }
        assert len(calls) == cap and calls[:-1] == [0]*(cap-1)
        assert calls[-1] == (fallback if accept_last else 0)
        rng.assert_exhausted()
    _, law, mass, tv = exact_clipped_law(native_spectrum, budget["clip_threshold"])
    acceptance = mass/budget["clip_threshold"]
    abort = (1-acceptance)**cap
    success = 1-abort
    target_histogram = Counter(value*value for value in native_spectrum)
    total_mass = sum((success*p for p in law), Fraction(0))+abort
    assert total_mass == 1
    unconditional_tv = (abort+sum((count*abs(
        success*Fraction(min(square, denominator), NATIVE_Q**2*mass)
        - Fraction(square, NATIVE_Q**2))
        for square, count in target_histogram.items()), Fraction(0)))/2
    assert abort <= budget["abort_probability_upper"]
    assert tv <= budget["conditional_tv_upper"]
    assert unconditional_tv <= tv+abort <= budget["unconditional_tv_upper"]


@pytest.mark.parametrize("sign", [-1, 1])
def test_mock_oracle_saturates_clipping_at_q_with_either_sign(sign):
    # Deliberately not a native Walsh oracle: this isolates saturation only.
    denominator = 240*NATIVE_Q
    rng = ScriptedRng([(NATIVE_Q, 1), (denominator, denominator-1)])
    result = access.sample_clipped_fourier(
        NATIVE_BITS, lambda bits, s, a: sign*NATIVE_Q, rng=rng)
    assert result["status"] == "ACCEPTED" and result["oracle_queries"] == 1
    assert result["oracle_correctness_assumed_not_verified"] is True
    assert result["polynomial_classical_walsh_access_established"] is False
    rng.assert_exhausted()


def test_none_rng_constructs_system_random_and_explicit_rng_does_not(
        native_spectrum, monkeypatch):
    frequency = next(a for a, value in enumerate(native_spectrum) if value < 0)
    denominator = 240*NATIVE_Q
    rng = ScriptedRng([(NATIVE_Q, frequency), (denominator, 0)])
    constructions = []

    def system_random():
        constructions.append(True)
        return rng

    monkeypatch.setattr(access, "SystemRandom", system_random)
    result = access.sample_clipped_fourier(NATIVE_BITS, native_oracle(native_spectrum, []))
    assert result["frequency"] == frequency and constructions == [True]
    rng.assert_exhausted()
    explicit = ScriptedRng([(NATIVE_Q, frequency), (denominator, 0)])
    access.sample_clipped_fourier(
        NATIVE_BITS, native_oracle(native_spectrum, []), rng=explicit)
    assert constructions == [True]
    explicit.assert_exhausted()


def test_large_n_mock_oracle_has_no_automatic_table_or_field_work(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("oracle-relative sampler attempted finite-table or field work")

    for module, names in (
        (access, ("finite_walsh_spectrum", "finite_fourier_report", "differential_count",
                  "gauss_block", "field", "element", "encoded", "walsh", "trace_indices")),
        (curve, ("finite_walsh_control", "finite_curve_count", "reciprocal_value",
                 "reciprocal_trace", "element", "field")),
        (balanced_signed_mpi, ("presentation", "walsh", "trace_indices")),
    ):
        for name in names:
            monkeypatch.setattr(module, name, forbidden)
    bits, q, calls = 127, 1 << 127, []
    budget = access.clipped_sampler_budget(bits)
    denominator = budget["clip_threshold"]*q

    def mock_exact_contract_oracle(n, s, frequency):
        # Exact integer output with valid shape; native correctness is NOT asserted.
        calls.append((n, s, frequency))
        return -(1 << 63)

    rng = ScriptedRng([(q, q-1), (denominator, (1 << 126)-1)])
    result = access.sample_clipped_fourier(bits, mock_exact_contract_oracle, rng=rng)
    assert calls == [(127, 31, q-1)]
    assert result == budget | {"status": "ACCEPTED", "frequency": q-1, "oracle_queries": 1}
    rng.assert_exhausted()
    with pytest.raises(ValueError):
        access.sample_clipped_fourier(bits, None, rng=ScriptedRng([]))


@pytest.mark.parametrize("bits", [True, False, 17.0, Fraction(17), "17", None,
                                  -17, 0, 2, 13, 16, 18, 21, 25, 49, 121, 128, 131])
def test_canonical_parameter_guards_before_rng_or_oracle(bits):
    for call in (
        lambda: access.differential_uniformity_bound(bits),
        lambda: access.clipped_sampler_budget(bits),
        lambda: access.sample_clipped_fourier(bits, lambda *args: pytest.fail("oracle called"),
                                             rng=ScriptedRng([])),
    ):
        with pytest.raises(ValueError):
            call()


@pytest.mark.parametrize("epsilon", [True, False, 0, 1, -1, 0.125, float("nan"),
                                     float("inf"), Decimal("0.125"), "1/8", None,
                                     Fraction(0), Fraction(-1, 8), Fraction(2, 3)])
def test_epsilon_strict_type_and_interval_guard(epsilon):
    for call in (
        lambda: access.clipped_sampler_budget(17, epsilon),
        lambda: access.sample_clipped_fourier(17, lambda *args: pytest.fail("oracle called"),
                                             epsilon, rng=ScriptedRng([])),
    ):
        with pytest.raises(ValueError):
            call()


@pytest.mark.parametrize("abort_bits", [True, False, 0, -1, 1.0, Fraction(1), "16", None])
def test_abort_bits_is_a_strict_positive_integer(abort_bits):
    for call in (
        lambda: access.clipped_sampler_budget(17, abort_bits=abort_bits),
        lambda: access.sample_clipped_fourier(17, lambda *args: pytest.fail("oracle called"),
                                             abort_bits=abort_bits, rng=ScriptedRng([])),
    ):
        with pytest.raises(ValueError):
            call()


@pytest.mark.parametrize("oracle", [None, True, 0, (), [], {}])
def test_caller_must_supply_callable_oracle_without_fallback(oracle):
    with pytest.raises(ValueError):
        access.sample_clipped_fourier(17, oracle, rng=ScriptedRng([]))


@pytest.mark.parametrize("value", [True, False, 2.0, Fraction(2), Decimal(2), "2", None,
                                   1, -1, NATIVE_Q+2, -NATIVE_Q-2])
def test_oracle_values_reject_nonintegers_odd_and_out_of_range_before_acceptance_draw(value):
    rng = ScriptedRng([(NATIVE_Q, 1)])
    with pytest.raises(ValueError):
        access.sample_clipped_fourier(17, lambda *args: value, rng=rng)
    rng.assert_exhausted()


@pytest.mark.parametrize("value", [-NATIVE_Q, -2, 2, NATIVE_Q])
def test_zero_frequency_requires_zero_walsh_value(value):
    rng = ScriptedRng([(NATIVE_Q, 0)])
    with pytest.raises(ValueError):
        access.sample_clipped_fourier(17, lambda *args: value, rng=rng)
    rng.assert_exhausted()


@pytest.mark.parametrize("frequency", [True, -1, NATIVE_Q, 1.0, Fraction(1)])
def test_invalid_random_frequency_does_not_reach_oracle(frequency):
    rng = ScriptedRng([(NATIVE_Q, frequency)])
    with pytest.raises(ValueError):
        access.sample_clipped_fourier(17, lambda *args: pytest.fail("oracle called"), rng=rng)
    rng.assert_exhausted()


@pytest.mark.parametrize("draw", [True, -1, 240*NATIVE_Q, 0.0, Fraction(0)])
def test_invalid_random_acceptance_draw_is_rejected(draw, native_spectrum):
    rng = ScriptedRng([(NATIVE_Q, 1), (240*NATIVE_Q, draw)])
    with pytest.raises(ValueError):
        access.sample_clipped_fourier(17, native_oracle(native_spectrum, []), rng=rng)
    rng.assert_exhausted()


def test_oracle_error_propagates_without_retry_or_fallback():
    rng = ScriptedRng([(NATIVE_Q, 1)])
    error = RuntimeError("external exact oracle unavailable")

    def failed_oracle(*args):
        raise error

    with pytest.raises(RuntimeError) as raised:
        access.sample_clipped_fourier(17, failed_oracle, rng=rng)
    assert raised.value is error
    rng.assert_exhausted()
