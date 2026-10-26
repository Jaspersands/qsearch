from dataclasses import replace
from fractions import Fraction
from itertools import product
from math import comb, exp, tanh
import random

import numpy as np
import pytest
from scipy.special import expit

from theorems import relative_gibbs_worldline as w


@pytest.mark.parametrize("slices", [1, 2, 5])
@pytest.mark.parametrize("gamma,dt", [(0.0, 0.2), (0.8, 0.1), (1.2, 0.0)])
def test_periodic_dynamic_program_matches_entire_conditional_law(slices, gamma, dt):
    field = np.linspace(-1.2, 0.7, slices)
    paths = list(product((1, -1), repeat=slices))
    exact, actual = [], []
    for path in paths:
        flips = sum(path[j] != path[(j+1) % slices] for j in range(slices))
        exact.append(exp(-dt*np.dot(field, path))*tanh(dt*gamma)**flips)
        returned, logp = w.ring_path(field, gamma, dt, prescribed=path)
        np.testing.assert_array_equal(returned, path)
        actual.append(exp(logp))
    exact = np.asarray(exact)/sum(exact)
    np.testing.assert_allclose(actual, exact, atol=2e-15)


@pytest.mark.parametrize("slices", [1, 2, 4])
@pytest.mark.parametrize("gamma,dt", [(0.0, 0.2), (0.8, 0.1), (1.2, 0.0)])
def test_outward_interval_periodic_path_encloses_exact_law_and_bounds_tv(slices, gamma, dt):
    field = [Fraction(k - 2, 3) for k in range(slices)]
    paths = list(product((1, -1), repeat=slices))
    for path in paths:
        _, logp = w.ring_path(field, gamma, dt, prescribed=path)
        exact_p = exp(logp)
        returned, (p_lo, p_hi), step_tv, coins = w.interval_ring_path(
            field, gamma, dt, bits=64, prescribed=path, max_coin_bits=96
        )
        np.testing.assert_array_equal(returned, path)
        assert coins == 0
        assert 0 <= p_lo <= p_hi <= 1
        assert float(p_lo) - 1e-15 <= exact_p <= float(p_hi) + 1e-15
        assert p_hi - p_lo < Fraction(1, 1 << 56)
        assert step_tv < Fraction(slices, 1 << 58)


def test_outward_interval_elementary_functions_and_monotonicity():
    for val in (Fraction(0), Fraction(1, 7), Fraction(-5, 3), Fraction(11, 4)):
        lo64, hi64 = w.exp_interval(val, 64)
        lo128, hi128 = w.exp_interval(val, 128)
        assert lo64 <= lo128 <= hi128 <= hi64
        assert abs(float((lo64 + hi64) / 2) - exp(float(val))) < 1e-14
    for val in (Fraction(0), Fraction(1, 9), Fraction(7, 5)):
        t_lo, t_hi = w.tanh_interval(val, 64)
        assert 0 <= t_lo <= t_hi <= 1
        assert abs(float((t_lo + t_hi) / 2) - tanh(float(val))) < 1e-15
    for val in (Fraction(-3, 2), Fraction(0), Fraction(5, 4)):
        l_lo, l_hi = w.logistic_interval(val, 64)
        assert 0 <= l_lo <= l_hi <= 1
        assert abs(float((l_lo + l_hi) / 2) - float(expit(float(val)))) < 1e-15


def test_certified_interval_update_audit_satisfies_per_update_budget():
    model = w.small_control()
    audit = w.certified_interval_update_audit(model, 0.08, 0.05, bits=64, max_coin_bits=96, seed=1986)
    assert audit["interval_conditional_TV_within_per_update_budget"] is True
    assert Fraction(audit["max_observed_single_update_TV_upper_exact"]) <= Fraction(audit["per_update_TV_tolerance_exact"])
    assert Fraction(audit["total_chain_update_rounding_TV_upper_exact"]) < Fraction(0.05) / 3
    assert audit["interval_arithmetic_certified"] is True
    assert audit["prng_is_not_a_certified_fair_coin_source"] is True


def test_interval_central_and_pinning_updates_match_exact_conditionals_and_abstain():
    model, beta, M = w.small_control(), 0.17, 2
    paths = np.array([[1, -1], [-1, -1], [1, 1]])
    central = np.array([1, -1])
    for a in range(model.r):
        _, (p_lo, p_hi), tv_up, _ = w.interval_central_update(model, a, paths, central, beta, bits=64)
        exact_plus = float(expit(-2 * beta * model.central_field(a, paths, central)))
        assert float(p_lo) - 1e-15 <= exact_plus <= float(p_hi) + 1e-15
        assert tv_up < Fraction(1, 1 << 60)

    class AlwaysZeroBits:
        def getrandbits(self, k):
            return 0

    forced_model = replace(w.small_control(), central=(-1, -1, -1), coupled=(0, 0, 0))
    res = w.interval_pin_given_paths(forced_model, 1.0, np.ones((3, 2), dtype=int), AlwaysZeroBits(), bits=64)
    assert res["ABSTAIN"] is True and res["rank"] == 2 and len(res["selected"]) == 3


def test_linear_work_path_handles_large_slice_count_without_enumeration():
    path, logp = w.ring_path(np.linspace(-3, 2, 4096), 0.6, 0.0001, np.random.default_rng(9))
    assert len(path) == 4096 and np.isfinite(logp)
    assert set(path) <= {-1, 1}


def test_worldline_marginal_is_symmetric_trotter_diagonal():
    model, beta, M = w.small_control(), 0.19, 2
    law = w.path_law(model, beta, M)
    marginal = np.zeros(2**(model.n+model.r))
    for state in np.ndindex(law.shape):
        word = tuple(value//(2**(M-1)) for value in state[:model.n])+state[n:] if False else tuple(value//(2**(M-1)) for value in state[:model.n])+state[model.n:]
        marginal[np.ravel_multi_index(word, (2,)*(model.n+model.r))] += law[state]
    np.testing.assert_allclose(marginal, np.diag(w.dense_gibbs(model, beta, M)), atol=3e-16)


def test_each_actual_update_has_the_correct_full_conditioning():
    model, beta, M = w.small_control(), 0.17, 2
    law = w.path_law(model, beta, M)
    paths = np.array(list(product((1, -1), repeat=M)))
    for state in np.ndindex(law.shape):
        q, R = paths[list(state[:model.n])], w.SPINS[list(state[model.n:])]
        for block in range(law.ndim):
            index = list(state)
            index[block] = slice(None)
            expected = law[tuple(index)].copy()
            expected /= expected.sum()
            if block < model.n:
                actual = [exp(w.ring_path(model.path_field(block, q, R), abs(model.transverse[block]),
                                         beta/M, prescribed=path)[1]) for path in paths]
            else:
                plus = expit(-2*beta*model.central_field(block-model.n, q, R))
                actual = [plus, 1-plus]
            np.testing.assert_allclose(actual, expected, atol=2e-15)


def test_influence_bound_covers_every_boundary_pair_and_detailed_balance():
    model, beta = w.small_control(), 0.12
    law = w.path_law(model, beta, 2)
    bound, actual = w.influence_bounds(model, beta), w.exact_influences(law)
    assert np.all(actual <= bound+2e-15)
    assert actual.max() > 0.09
    np.testing.assert_array_equal(bound, bound.T)
    P, pi = w.exact_transition(law), law.ravel()
    np.testing.assert_allclose(P.sum(axis=1), 1, atol=1e-15)
    np.testing.assert_allclose(pi[:, None]*P, pi[None, :]*P.T, atol=1e-16)
    budget = w.sampling_budget(model, beta, 0.1)
    worst = abs(np.linalg.matrix_power(P, budget["updates"])-pi[None, :]).sum(axis=1).max()/2
    assert worst <= budget["mixing_TV_bound"]+1e-13


def test_transverse_sign_gauge_preserves_target_diagonal():
    model = w.small_control()
    positive = replace(model, transverse=tuple(abs(x) for x in model.transverse))
    np.testing.assert_allclose(np.diag(w.dense_gibbs(model, 0.3)), np.diag(w.dense_gibbs(positive, 0.3)))
    # Independent original signed Hamiltonian, not the gauge helper itself.
    V, G = w.dense_target(model)
    from scipy.linalg import expm
    for i, coefficient in enumerate(model.transverse):
        bit = 1 << (model.n+model.r-1-i)
        for z in range(len(G)):
            G[z, z ^ bit] = -coefficient
    rho = expm(-0.3*(V-G))
    rho /= np.trace(rho)
    np.testing.assert_allclose(np.diag(rho), np.diag(w.dense_gibbs(model, 0.3)), atol=2e-16)


def test_trotter_bound_on_noncommuting_target_and_convergence():
    model, beta = w.small_control(), 0.18
    V, G = w.dense_target(model)
    assert np.linalg.norm(V @ G-G @ V) > 1
    exact, previous = w.dense_gibbs(model, beta), float("inf")
    for M in (1, 2, 4, 8, 16):
        distance = abs(np.linalg.eigvalsh(exact-w.dense_gibbs(model, beta, M))).sum()/2
        assert 0 < distance < previous
        assert distance < w.trotter_bound(beta, model.norm_bound, M)
        previous = distance


def test_thermodynamic_fields_and_transverse_strength_do_not_enter_influence():
    model = w.small_control()
    changed = replace(model, longitudinal=(100.0, -100.0, 0.0), transverse=(0.0, 100.0, -200.0))
    np.testing.assert_array_equal(w.influence_bounds(model, 0.2), w.influence_bounds(changed, 0.2))
    assert w.sampling_budget(changed, 0.2, 0.1)["slices"] > w.sampling_budget(model, 0.2, 0.1)["slices"]


def test_shared_parities_aggregate_before_tanh():
    model = w.ChainTarget(((1, 1), (1, 1)), (1, 1), (0, 0), (2, -3), (4, -5), (0,))
    assert w.influence_bounds(model, 0.1)[2, 3] == tanh(1.4)


def test_zero_transverse_and_infinite_temperature_remain_supported():
    model = replace(w.small_control(), transverse=(0, 0, 0))
    result = w.sample(model, 0.0, 0.2, seed=2)
    assert result["budget"]["Trotter_TV_bound"] == 0
    assert result["budget"]["alpha"] == 0
    assert result["budget"]["slices"] == 1


def test_live_sampler_never_calls_dense_or_exact_pool_helpers(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("exponential oracle reached")
    monkeypatch.setattr(w, "dense_gibbs", fail)
    monkeypatch.setattr(w, "dense_target", fail)
    monkeypatch.setattr(w, "path_law", fail)
    result = w.sample(w.small_control(), 0.08, 0.2)
    assert result["dense_or_counting_oracle_calls"] == 0
    assert not result["sample_has_rigorous_floating_point_error_certificate"]
    assert not result["prepared_quantum_state"]
    budget = result["budget"]
    assert budget["mixing_TV_bound"]+budget["Trotter_TV_bound"] < 2*0.2/3


def test_failed_classical_certificate_is_not_a_hardness_claim():
    with pytest.raises(ValueError, match="NO mixing certificate"):
        w.sample(w.small_control(), 20, 0.1)
    # Higher incidence can evade this comparator; no universal closure.
    assert w.regular_influence_bound(5, 10, 0.022) > 1


@pytest.mark.parametrize("n,rank", [(7, 3), (32, 16), (256, 128), (4, 0), (4, 4)])
def test_packing_envelope_is_exact_necessary_inequality(n, rank):
    D = w.packing_radius_upper(n, rank)
    assert sum(comb(n, j) for j in range(D+1)) <= 2**rank
    if D < n:
        assert sum(comb(n, j) for j in range(D+2)) > 2**rank


@pytest.mark.parametrize("n", [64, 256, 1024, 4096])
def test_published_optimistic_regular_window_is_covered(n):
    result = w.quantum_window_upper(n, n//2, 0.005)
    assert w.regular_influence_bound(3, 6, result["optimistic_beta_upper"]) < 1
    assert not result["actual_decoder_supplied"]
    assert not result["bound_on_ALL_quantum_algorithms"]


def test_asymptotic_three_six_window_has_rational_margin():
    assert 2**20 > 7**7  # H_2(1/8) > 1/2, without a floating entropy claim.
    assert w.regular_influence_bound(3, 6, 1/40) < 3/4


def test_regular_control_keeps_actual_input_and_no_decoder_promise():
    model = w.regular_control()
    F = np.array(model.F)
    np.testing.assert_array_equal(F.sum(axis=0), 3)
    np.testing.assert_array_equal(F.sum(axis=1), 6)
    assert model.norm_bound == 5*model.n-1
    assert np.max(w.influence_bounds(model, 0.02).sum(axis=0)) <= w.regular_influence_bound(3, 6, 0.02)


@pytest.mark.parametrize("beta", [0.08, 0.7])
def test_correlated_source_pinning_full_law_and_abstain(beta):
    model = w.small_control()
    result = w.exact_pinning_control(model, beta)
    bound = w.pinning_error_bound(model, beta, 3)
    assert abs(result["output_mass"]-1) < 2e-14
    assert result["ABSTAIN_mass"] > 0
    assert result["TV_including_ABSTAIN"] <= bound["pinning_TV_bound_including_ABSTAIN"]+1e-14
    assert result["TV_including_ABSTAIN"] >= result["ABSTAIN_mass"]-1e-14
    assert result["TV_after_UNCHARGED_postselection_countercontrol"] > 1e-6


def test_dependency_weight_sum_identity_counts_all_kernel_vectors():
    model = w.small_control()
    probabilities = np.array([0.12, 0.31, 0.27])
    expected = 0
    for flags in product((0, 1), repeat=3):
        selected = tuple(i for i, v in enumerate(flags) if v)
        mass = np.prod(np.where(flags, probabilities, 1-probabilities))
        system = w.pin_system(model, selected, (1, 1, 1))
        expected += mass*(2**(len(selected)-system["rank"])-1)
    # The only nonzero kernel vector is 111.
    assert abs(expected-np.prod(probabilities)) < 1e-16


def test_dependent_consistent_pin_set_is_not_silently_accepted():
    class ForceAllPins:
        def random(self):
            return 0.0
    model = replace(w.small_control(), central=(-1, -1, -1), coupled=(0, 0, 0))
    result = w.pin_given_paths(model, 1.0, np.ones((3, 2)), ForceAllPins())
    assert result["ABSTAIN"] and result["rank"] == 2 and len(result["selected"]) == 3


def test_uniform_affine_pin_solver_keeps_all_free_coordinates():
    model = w.small_control()
    system = w.pin_system(model, (1,), (-1, -1, -1))
    samples = {w.uniform_affine_solution(system, model.r, random.Random(i)) for i in range(32)}
    assert samples == {1, 2}


def test_pinning_distance_is_a_premise_and_unknown_regime_stays_unknown():
    result = w.pinning_error_bound(w.repetition_control(), 2, 1)
    assert result["pinning_TV_bound_including_ABSTAIN"] == 1
    assert not result["distance_verified_by_this_function"]
    with pytest.raises(ValueError):
        w.pinning_error_bound(w.small_control(), 0.1, 0)


def test_pinning_bypasses_direct_target_mixing_obstruction():
    model = w.repetition_control()
    assert w.influence_bounds(model, 0.03).sum(axis=0).max() > 1
    assert w.influence_bounds(w.identity_source(model), 0.03).sum(axis=0).max() < 0.1
    bound = w.pinning_error_bound(model, 0.03, model.n)
    assert bound["pinning_TV_bound_including_ABSTAIN"] < 1e-38
    assert w.quantum_window_upper(32, 31, 0.005)["optimistic_beta_upper"] > 0.03


def test_source_pinning_uses_no_count_or_target_sampler(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("target enumeration is forbidden")
    monkeypatch.setattr(w, "dense_gibbs", fail)
    monkeypatch.setattr(w, "path_law", fail)
    monkeypatch.setattr(w, "sample", fail)
    result = w.sample_via_source(w.small_control(), 0.05, 0.2, 3)
    assert result["source_central_sample_discarded"]
    assert not result["retry_after_ABSTAIN"]
    assert not result["prepared_TFD"]
    assert result["dense_or_counting_oracle_calls"] == 0
    assert result["analytic_TV_bound_excluding_roundoff"] < 0.2


def test_matching_diagonal_does_not_prepare_the_quantum_gibbs_state():
    rho = w.dense_gibbs(w.small_control(), 0.3)
    dephased = np.diag(np.diag(rho))
    assert abs(np.linalg.eigvalsh(rho-dephased)).sum()/2 > 0.1


def test_source_correlations_cannot_be_dropped(monkeypatch):
    model, beta = w.small_control(), 0.08
    good = w.exact_pinning_control(model, beta)
    original = w.identity_source
    def wrong_source(target):
        return replace(original(target), longitudinal=(0, 0, 0), coupled=(0, 0, 0), bonds=(0, 0))
    monkeypatch.setattr(w, "identity_source", wrong_source)
    bad = w.exact_pinning_control(model, beta)
    bound = w.pinning_error_bound(model, beta, 3)["pinning_TV_bound_including_ABSTAIN"]
    assert good["TV_including_ABSTAIN"] < bound < bad["TV_including_ABSTAIN"]


@pytest.mark.parametrize("operation", [
    lambda: w.influence_bounds(w.small_control(), -1),
    lambda: w.sampling_budget(w.small_control(), 0.1, 0),
    lambda: w.quantum_window_upper(3, 2, 0),
    lambda: w.packing_radius_upper(3, 4),
    lambda: w.trotter_bound(0.1, 1, 0),
    lambda: w.path_law(w.small_control(), 0.1, 10),
    lambda: w.dense_target(w.regular_control()),
    lambda: w.ring_path([1], 1, 1),
    lambda: replace(w.small_control(), F=((1, 2, 0),)),
    lambda: replace(w.small_control(), coupled=(0, 1)),
    lambda: w.exp_interval(1, bits=8),
    lambda: w.tanh_interval(-1, bits=32),
    lambda: w.draw_interval_bernoulli((Fraction(2, 3), Fraction(1, 3)), random.Random(0)),
])
def test_invalid_contracts_fail_closed(operation):
    with pytest.raises(ValueError):
        operation()
