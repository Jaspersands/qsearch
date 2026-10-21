"""Local variable dependencies, biased coins, native resampling and theorem scope."""

from fractions import Fraction
import hashlib
from itertools import product
import json
import random

from flint import fmpz
import pytest

import theorems.interval_local_lemma as module
from theorems.interval_local_lemma import (REPORT, certificate, check_local_lemma,
                                        event_variables, exact_event_model, radius,
                                        run_controls, solve, target_certificate)
from theorems.interval_split_fibers import public_frame
from theorems.interval_subgroup_rounding import coordinates, frame


def moments(p, d, word):
    return [sum(pow(x, j, p) * a for x, a in enumerate(word)) % p for j in range(d)]


def residual(p, y, w, z):
    return [y[x] - z[0] - sum(z[t + 1] * w[(x - t) % p] for t in range(p - 1)) for x in range(p)]


def test_fixing_the_constant_is_essential_to_the_dependency_bound():
    model = frame(101, 1)
    p, s = model["p"], len(model["support"])
    dependencies = [set(event_variables(model, x)) for x in range(p)]
    assert all(0 not in variables and len(variables) <= s for variables in dependencies)
    degree = max(sum(bool(a & b) for j, b in enumerate(dependencies) if j != i)
                 for i, a in enumerate(dependencies))
    assert degree <= s * (s - 1) == 2 < p - 1
    with_global_coin = [variables | {0} for variables in dependencies]
    assert all(a & b for a in with_global_coin for b in with_global_coin)
    assert p - 1 > s * (s - 1)


@pytest.mark.parametrize("p,ell,torus", [(31, 5, "split"), (47, 6, "nonsplit"), (47, 12, "nonsplit")])
def test_exact_event_variable_sets_and_occurrences_including_weighted_frames(p, ell, torus):
    model = frame(p, ell, torus)
    s, w = len(model["support"]), model["waveform"]
    sets = []
    for x in range(p):
        expected = {t + 1 for t in range(p - 1) if w[(x - t) % p]}
        assert set(event_variables(model, x)) == expected
        sets.append(expected)
    assert all(sum(i in variables for variables in sets) == s for i in range(1, p))
    actual = max(sum(bool(a & b) for j, b in enumerate(sets) if j != i) for i, a in enumerate(sets))
    assert actual <= min(p - 1, s * (s - 1))


def test_exact_biased_rounding_law_pays_for_the_fixed_constant_half_offset():
    p, ell, y = 11, 3, [5] + [0] * 10
    model = frame(p, ell, "nonsplit")
    nums, D = coordinates(model, y)
    z0 = (2 * nums[0] + D) // (2 * D)
    bias = Fraction(nums[0], D) - z0
    assert 0 < bias <= Fraction(1, 2)
    choices = []
    for a in nums[1:]:
        q, r = divmod(a, D)
        choices.append([(q, Fraction(D - r, D))] + ([(q + 1, Fraction(r, D))] if r else []))
    means = [Fraction(0)] * p
    failures = [Fraction(0)] * p
    bound = certificate(p, len(model["support"]), model["squared_waveform_norm"], 3)
    for outcome in product(*choices):
        probability = 1
        for _, prob in outcome:
            probability *= prob
        raw = residual(p, y, model["waveform"], [z0] + [t[0] for t in outcome])
        for x, value in enumerate(raw):
            means[x] += probability * value
            failures[x] += probability * int(abs((value + p // 2) % p - p // 2) > 3)
    assert means == [bias] * p  # NOT mean zero after fixing the constant.
    assert all(q <= Fraction(bound["per_bad_event_probability_upper_exact"]) for q in failures)


def test_symmetric_local_lemma_and_expected_runtime_are_verified_with_rationals():
    for p, s, S in ((347, 16, 16), (1019, 32, 32), (2017, 64, 64), (65537, 64, 64)):
        u = radius(p, s, S)
        c = certificate(p, s, S, u, resampling_budget=100)
        degree = min(p - 1, s * (s - 1))
        assert c["dependency_degree_upper"] == degree
        q = Fraction(2, 1 << c["integer_half_offset_tail_exponent_floor"])
        x = Fraction(c["MT_x_exact"])
        rhs = x * (1 - x) ** degree
        assert q <= Fraction(c["symmetric_LLL_rhs_lower_exact"]) <= rhs
        assert c["uniform_all_target_local_lemma_criterion_certified"]
        assert Fraction(c["expected_total_resampling_steps_upper_exact"]) == Fraction(p, degree)
        assert Fraction(c["ideal_coin_budget_failure_Markov_upper_exact"]) >= min(Fraction(1), Fraction(p, degree * 100))
    assert radius(65537, 64, 64) == radius((1 << 127) - 1, 64, 64) == 22
    # Field size no longer enters once p exceeds the support dependency bound.
    assert radius((1 << 61) - 1, 512, 512) == 73 < 256 // 2


def test_all_resampling_coins_use_the_actual_denominator_and_never_the_constant(monkeypatch):
    _, model = public_frame(347, 8)
    saved = json.loads(REPORT.read_text())["uncertified_aggressive_resampling_control"]
    actual = random.Random
    draws = []

    class Tracking:
        def __init__(self, seed):
            self.rng = actual(seed)

        def randrange(self, upper):
            draws.append(upper)
            return self.rng.randrange(upper)

    monkeypatch.setattr(module.random, "Random", Tracking)
    r = solve(model, 8, 3, saved["public_particular_word"], resampling_budget=2)
    D = int(fmpz(r["coordinate_common_denominator_decimal"]))
    assert D > 347 and set(draws) == {D}
    assert len(draws) == 346 + sum(len(t["resampled_coefficient_indices"]) for t in r["resampling_transcript"])
    assert all(0 not in t["resampled_coefficient_indices"] for t in r["resampling_transcript"])
    assert r["constant_coefficient_resamples"] == 0


def test_independent_transcript_replay_checks_every_local_update_and_native_syndrome():
    r = json.loads(REPORT.read_text())["uncertified_aggressive_resampling_control"]
    p, ell, u, w, y = r["p"], r["ell"], r["u"], r["waveform"], r["public_particular_word"]
    z = [int(fmpz(a)) for a in r["initial_coefficients_decimal"]]
    nums, D = [int(fmpz(a)) for a in r["coordinate_numerators_decimal"]], int(fmpz(r["coordinate_common_denominator_decimal"]))
    constant = z[0]
    assert r["resampling_steps"] > 0
    for t in r["resampling_transcript"]:
        raw = residual(p, y, w, z)
        x = t["bad_coordinate"]
        assert abs((raw[x] + p // 2) % p - p // 2) > u
        variables = [i + 1 for i in range(p - 1) if w[(x - i) % p]]
        assert t["resampled_coefficient_indices"] == variables
        affected = set()
        for i, bit in zip(variables, t["new_ceil_bits"]):
            z[i] = nums[i] // D + bit
            affected.update((a + i - 1) % p for a, value in enumerate(w) if value)
        assert t["affected_columns"] == sorted(affected)
        raw = residual(p, y, w, z)
        assert moments(p, ell, raw) == r["target_syndrome"]
        assert sum(abs((a + p // 2) % p - p // 2) > u for a in raw) == t["remaining_bad_coordinates"]
        assert z[0] == constant
    assert z == [int(fmpz(a)) for a in r["final_coefficients_decimal"]]
    assert not r["certificate"]["uniform_all_target_local_lemma_criterion_certified"]
    assert r["certificate"]["expected_total_resampling_steps_upper_exact"] is None


def test_budget_exhaustion_is_not_hardness_or_a_false_uniform_guarantee():
    saved = json.loads(REPORT.read_text())["uncertified_aggressive_resampling_control"]
    _, model = public_frame(347, 8)
    r = solve(model, 8, 3, saved["public_particular_word"], resampling_budget=1)
    assert r["solution"] is None and r["remaining_bad_coordinates"]
    assert r["status"] == "LLL_RESAMPLING_BUDGET_EXHAUSTED_NOT_HARDNESS"
    assert r["certificate"]["ideal_coin_budget_failure_Markov_upper_exact"] is None
    assert r["target_rerolls"] == 0


def test_saved_report_native_polynomial_replay_and_analytic_scope():
    r = json.loads(REPORT.read_text())
    assert r == run_controls()
    assert r["source_sha256"] == hashlib.sha256(module.Path(module.__file__).read_bytes()).hexdigest()
    assert r["all_certified_native_controls_verified"]
    for row in r["controls"] + [r["uncertified_aggressive_resampling_control"]]:
        if row["solution"] is None:
            continue
        p, y, d = row["p"], row["public_particular_word"], row["d"]
        e, P = row["solution"]["centered_affine_witness"], row["solution"]["polynomial_coefficients"]
        assert max(map(abs, e)) <= row["u"]
        assert moments(p, d, e) == moments(p, d, y) == row["target_syndrome"]
        assert abs(Fraction(row["constant_rounding_error_exact"])) <= Fraction(1, 2)
        for x in range(p):
            value = 0
            for a in reversed(P):
                value = (value * x + a) % p
            assert (y[x] - e[x] - value) % p == 0
    for row in r["analytic_parameter_only_controls"]:
        assert row["no_full_field_frame_or_native_target_executed"]
        assert row["certificate"]["uniform_all_target_local_lemma_criterion_certified"]
        assert row["certificate"]["pure_parameters_do_not_construct_a_frame"]
        if row["conditional_frame_family"] == "fiber_Weil":
            assert row["public_setup_Weil_certificate"]["every_distinct_constraint_set_has_a_legal_shift_certified"]
        else:
            assert row["proper_torus_divisor_checked"]
    assert not r["novelty_quantum_speedup_or_prescribed_sampling_claimed"]


@pytest.mark.parametrize("u", [0, 2, 5])
def test_local_DP_matches_independent_full_product_distribution_with_weighted_rows(u):
    p, y = 11, [5] + [0] * 10
    model = frame(p, 3, "nonsplit")
    assert 2 in map(abs, model["waveform"])
    nums, D = coordinates(model, y)
    constant = (2 * nums[0] + D) // (2 * D)
    choices = []
    for a in nums[1:]:
        floor, remainder = divmod(a, D)
        choices.append([(floor, Fraction(D - remainder, D))]
                       + ([(floor + 1, Fraction(remainder, D))] if remainder else []))
    expected = [Fraction(0)] * p
    for outcome in product(*choices):
        mass = Fraction(1)
        for _, probability in outcome:
            mass *= probability
        raw = residual(p, y, model["waveform"], [constant] + [a for a, _ in outcome])
        for x, value in enumerate(raw):
            expected[x] += mass * (abs((value + p // 2) % p - p // 2) > u)
    probabilities, variables, costs = exact_event_model(model, 3, u, y)
    assert probabilities == expected
    for x, active in enumerate(variables):
        assert active == frozenset(t + 1 for t in range(p - 1)
                                   if model["waveform"][(x - t) % p] and nums[t + 1] % D)
    assert costs["max_DP_states"] <= costs["waveform_L1_span_upper"] + 1
    assert costs["max_DP_integer_span"] <= costs["waveform_L1_span_upper"]
    assert costs["max_unreduced_probability_denominator_bits"] > D.bit_length()


def test_asymmetric_target_certificate_beats_a_worst_marginal_substitution():
    model, y = frame(11, 3, "nonsplit"), [5] + [0] * 10
    probabilities, variables, _ = exact_event_model(model, 3, 2, y)
    record = target_certificate(model, 3, 2, y)
    assert record["fixed_target_local_lemma_criterion_certified"]
    assert record["witness_selection"] == "asymmetric_twice_outward_marginals"
    neighbours = [{j for j, other in enumerate(variables) if j != i and other & active}
                  for i, active in enumerate(variables)]
    degree = max(map(len, neighbours))
    x = Fraction(1, degree + 1)
    assert max(probabilities) > x * (1 - x) ** degree
    witnesses = [Fraction(a) for a in record["LLL_witnesses_exact"]]
    for i, q in enumerate(probabilities):
        rhs = witnesses[i]
        for j in neighbours[i]:
            rhs *= 1 - witnesses[j]
        assert q <= Fraction(record["event_probability_upper_128bit_dyadic"][i]) <= rhs
    expected = sum((a / (1 - a) for a in witnesses), Fraction(0))
    assert expected <= Fraction(record["expected_total_resampling_steps_upper_exact"])
    assert min(Fraction(1), expected / 4096) <= Fraction(record["ideal_coin_budget_failure_Markov_upper_exact"])


def test_certificate_does_not_use_seed_frequency_or_promote_zero_event_instances(monkeypatch):
    def forbid_rng(*args, **kwargs):
        raise AssertionError("a probability certificate cannot depend on PRNG outcomes")

    monkeypatch.setattr(module.random, "Random", forbid_rng)
    model = frame(11, 3, "nonsplit")
    zero = target_certificate(model, 3, 0, [0] * 11, resampling_budget=1)
    bad = target_certificate(model, 3, 0, [5] + [0] * 10, resampling_budget=1)
    assert zero["fixed_target_local_lemma_criterion_certified"]
    assert zero["positive_probability_events"] == zero["actual_dependency_degree_upper"] == 0
    assert zero["LLL_witnesses_exact"] == ["0"] * 11
    assert zero["expected_total_resampling_steps_upper_exact"] == "0"
    assert not bad["fixed_target_local_lemma_criterion_certified"]
    assert bad["expected_total_resampling_steps_upper_exact"] is None
    assert bad["ideal_coin_budget_failure_Markov_upper_exact"] is None
    assert bad["input_sha256"] != zero["input_sha256"]
    assert "NOT_UNIFORM" in zero["scope"]


def test_inequality_checker_rejects_invalid_graphs_and_uncertain_witnesses():
    assert check_local_lemma([Fraction(0)], [set()], [Fraction(0)])
    assert check_local_lemma([Fraction(1, 4)], [set()], [Fraction(1, 2)])
    assert not check_local_lemma([Fraction(1)], [set()], [Fraction(1, 2)])
    assert not check_local_lemma([Fraction(1, 4)], [set()], [Fraction(1)])
    with pytest.raises(ValueError, match="symmetric"):
        check_local_lemma([Fraction(1, 4)] * 2, [{1}, set()], [Fraction(1, 2)] * 2)
    with pytest.raises(ValueError, match="loop-free"):
        check_local_lemma([Fraction(1, 4)], [{0}], [Fraction(1, 2)])
    with pytest.raises(ValueError, match="exact rational"):
        check_local_lemma([Fraction(1, 4)], [set()], [0.5])
    with pytest.raises(ValueError, match="removed"):
        check_local_lemma([Fraction(0)], [set()], [Fraction(1, 2)])


def test_certified_target_really_resamples_a_violated_event_without_changing_the_word(monkeypatch):
    model, y = frame(11, 3, "nonsplit"), [5] + [0] * 10
    nums, D = coordinates(model, y)
    assert nums[1] % D

    class ForcedPositiveMassTranscript:
        def __init__(self, seed):
            self.count = 0

        def randrange(self, denominator):
            assert denominator == D
            self.count += 1
            return 0 if self.count == 1 else D - 1

    monkeypatch.setattr(module.random, "Random", ForcedPositiveMassTranscript)
    row = solve(model, 3, 2, y, resampling_budget=1, certify_target=True)
    assert row["public_particular_word"] == y and row["target_rerolls"] == 0
    assert row["initial_bad_coordinates"] == [6] and row["resampling_steps"] == 1
    assert row["resampling_transcript"][0]["resampled_coefficient_indices"] == [1, 2, 5, 7, 8]
    assert row["fixed_target_certificate"]["fixed_target_local_lemma_criterion_certified"]
    assert row["solution"] is not None and row["remaining_bad_coordinates"] == []
    assert moments(11, 3, row["solution"]["centered_affine_witness"]) == moments(11, 3, y)


def test_original_large_target_gains_a_certificate_but_narrower_success_stays_uncertified():
    report = json.loads(REPORT.read_text())
    original = report["uncertified_aggressive_resampling_control"]
    low, high = report["original_target_exact_probability_controls"]
    for row in (low, high):
        assert row["public_particular_word"] == original["public_particular_word"]
        assert row["target_rerolls"] == 0 and row["solution"] is not None
        assert moments(row["p"], row["d"], row["solution"]["centered_affine_witness"]) == row["target_syndrome"]
        assert not row["certificate"]["uniform_all_target_local_lemma_criterion_certified"]
        assert row["fixed_target_certificate"]["costs"]["all_distributions_exactly_normalized"]
        assert row["fixed_target_certificate"]["actual_dependency_degree_upper"] == 106
    assert low["u"] == 3 and low["resampling_steps"] == 16
    assert not low["fixed_target_certificate"]["fixed_target_local_lemma_criterion_certified"]
    assert low["fixed_target_certificate"]["expected_total_resampling_steps_upper_exact"] is None
    assert high["u"] == 5 < radius(347, 16, 16) == 9
    assert high["fixed_target_certificate"]["fixed_target_local_lemma_criterion_certified"]
    model = public_frame(347, 8)[1]
    probabilities, variables, _ = exact_event_model(model, 8, high["u"], high["public_particular_word"])
    upper = list(map(Fraction, high["fixed_target_certificate"]["event_probability_upper_128bit_dyadic"]))
    witnesses = list(map(Fraction, high["fixed_target_certificate"]["LLL_witnesses_exact"]))
    for i, q in enumerate(probabilities):
        rhs = witnesses[i]
        if not q:
            assert rhs == 0
            continue
        for j, other in enumerate(variables):
            if j != i and probabilities[j] and variables[i] & other:
                rhs *= 1 - witnesses[j]
        assert q <= upper[i] <= rhs
