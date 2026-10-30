from fractions import Fraction as Q
from itertools import product
from random import Random

import pytest

from decoded_transfer import (DecodedSampler, PauliEstimator, complex_partner, d,
                              old, squared)
from decoded_controls import (accepted_trial_law, exact_importance_moments,
                              observable_mean, output_law)
from transfer_access import TransferAccess, fraction, gaussian
from tree_controls import direct_native_vector
from tree_sampler import Decomposition


def setup(paulis, n=2, *, couplings=None, parameters=None):
    m = len(paulis)
    couplings = [Q((-1)**i, i+1) for i in range(m)] if couplings is None else couplings
    parameters = [(Q(1, 3), Q(1, 7)), (Q(-1, 5), Q(2, 9))] if parameters is None else parameters
    model = d.Physical.create(n, paulis, couplings, Q(1, 2))
    decomposition = Decomposition(m, model.pilot.edges, [set(range(m))], [], independence_bound=m)
    access = TransferAccess(decomposition, couplings, parameters)
    representatives = {model.label(y): y for y in reversed(range(1 << m))}
    decoder = lambda syndrome: representatives.get(syndrome, 0)
    return model, decoder, access


FIXTURES = [((1, 0, 0), (0, 1, 0), (1, 1, 1)),
            ((1, 0, 0), (1, 0, 0), (0, 1, 0)),
            ((0, 1, 0), (0, 2, 0), (0, 3, 0)),
            ((1, 0, 0), (0, 3, 0), (2, 0, 0))]


@pytest.mark.parametrize("paulis", FIXTURES)
def test_signed_amplitude_contraction_matches_direct_actions_and_two_replica_norm(paulis):
    model, _, access = setup(paulis)
    direct = direct_native_vector(access.couplings, model.pilot.edges, access.parameters)
    for y, expected in enumerate(direct):
        assert access.amplitude(y) == expected
        assert access.probability(y) == access.sampler.probability(tuple(y >> i & 1 for i in range(access.m)))
    assert sum(map(squared, direct)) == access.norm_squared


@pytest.mark.parametrize("paulis", FIXTURES)
@pytest.mark.parametrize("decoder_kind", ["section", "bad-zero", "arbitrary"])
def test_entire_actual_physical_output_and_exact_one_over_fiber_acceptance(paulis, decoder_kind):
    model, decoder, access = setup(paulis)
    if decoder_kind == "bad-zero":
        decoder = lambda syndrome: 0
    elif decoder_kind == "arbitrary":
        rng = Random(908)
        table = [rng.randrange(1 << access.m) for _ in range(1 << (2*model.n))]
        decoder = table.__getitem__
    sampler = DecodedSampler(model, decoder, access)
    accepted = accepted_trial_law(sampler)
    target = output_law(model, decoder, access.parameters)
    bound = sampler.plan["fiber_bound"]
    assert sum(target.values()) == 1
    assert sum(accepted.values()) == Q(1, bound)
    assert {event: p*bound for event, p in accepted.items() if p} == {event: p for event, p in target.items() if p}
    assert not sampler.plan["average_sign_bound_required"]
    assert not sampler.plan["gibbs_accuracy_certified"]


@pytest.mark.parametrize("paulis", FIXTURES)
@pytest.mark.parametrize("observable", [(1, 0, 0), (0, 1, 0), (2, 3, 1), (3, 0, 0), (0, 0, 0)])
def test_complex_observable_mean_and_second_moment_against_direct_state(paulis, observable):
    model, decoder, access = setup(paulis)
    for actual_decoder in (decoder, lambda syndrome: 0):
        estimator = PauliEstimator(model, actual_decoder, access, observable)
        mean, second = exact_importance_moments(estimator)
        assert mean == observable_mean(model, actual_decoder, access.parameters, observable)
        assert second <= 1


def test_imaginary_partner_phase_cannot_be_discarded_for_complex_pilot():
    model, _, access = setup(((1, 0, 0), (0, 3, 0), (2, 0, 0)))
    grouped = {model.label(y): y for y in (1, 7)}
    decoder = lambda syndrome: grouped.get(syndrome, 0)
    observable = (2, 3, 1)
    estimator = PauliEstimator(model, decoder, access, observable)
    mean, _ = exact_importance_moments(estimator)
    assert mean == observable_mean(model, decoder, access.parameters, observable)
    assert mean != 0
    discarded = Q(0)
    found_imaginary_contribution = False
    for y in range(8):
        if not access.probability(y):
            continue
        match = complex_partner(model, decoder, observable, y)
        if match is not None and match[1].y and estimator.value(y):
            found_imaginary_contribution = True
        if match is not None and not match[1].y:
            discarded += access.probability(y)*estimator.value(y)
    assert found_imaginary_contribution and discarded != mean


def test_importance_weights_are_not_clipped_at_one():
    tiny = Q(1, 10**80)
    model, decoder, access = setup(((0, 1, 0),), n=1, couplings=[1], parameters=[-tiny])
    estimator = PauliEstimator(model, decoder, access, (0, 1, 0))
    assert estimator.value(1) == 1/tiny
    mean, second = exact_importance_moments(estimator)
    assert mean == 2*tiny/(1+tiny*tiny) and second == 1
    clipped = sum(access.probability(y)*min(estimator.value(y), 1) for y in (0, 1))
    assert clipped < mean*Q(3, 4)


def test_actual_output_differs_from_bell_label_pushforward():
    model, decoder, access = setup(((0, 1, 0),), n=1, couplings=[1], parameters=[Q(1, 2)])
    sampler = DecodedSampler(model, decoder, access)
    target = output_law(model, decoder, access.parameters)
    assert sum(p for (_, left, _), p in target.items() if left == 0) == Q(1, 10)
    assert sampler.proposal(0, 0)["acceptance"] == Q(1, 10)
    assert sampler.proposal(0, 1)["acceptance"] == Q(9, 10)


def test_zero_amplitudes_bad_decoders_and_out_of_image_rows():
    model, decoder, access = setup(((1, 0, 0),), n=1, couplings=[1], parameters=[])
    assert not access.amplitude(1)
    estimator = PauliEstimator(model, decoder, access, (0, 1, 0))
    assert estimator.value(0) == 0
    with pytest.raises(ValueError, match="zero source"):
        estimator.value(1)
    with pytest.raises(ValueError, match="m-bit"):
        complex_partner(model, lambda syndrome: 2, (1, 0, 0), 0)
    with pytest.raises(ValueError, match="zero-probability"):
        DecodedSampler(model, lambda syndrome: 0, access).proposal(1, 0)


def test_large_fiber_refusal_does_not_disable_pauli_estimator():
    n = 20
    model = d.Physical.create(n, [(0, 1 << i, 0) for i in range(n)], [1]*n, Q(1, 2))
    dec = lambda syndrome: syndrome >> n
    decomposition = Decomposition(n, [], [{i} for i in range(n)], [(i, i+1) for i in range(n-1)], independence_bound=1)
    access = TransferAccess(decomposition, [1]*n, [Q(1, 4)])
    with pytest.raises(ValueError, match="fiber"):
        DecodedSampler(model, dec, access, max_fiber=8)
    estimator = PauliEstimator(model, dec, access, (0, 1, 0))
    assert estimator.plan()["fiber_enumeration_required"] is False
    assert estimator.value(0) == Q(-1, 4)


def test_live_samples_are_reproducible_and_all_attempts_are_charged():
    model, decoder, access = setup(FIXTURES[0])
    sampler = DecodedSampler(model, decoder, access)
    target = output_law(model, decoder, access.parameters)
    for seed in range(10):
        a, b = sampler.sample(Random(seed)), sampler.sample(Random(seed))
        assert a == b
        if a["status"] == "sample":
            assert target[(a["residue"], a["left"], a["right"])] > 0
        assert a["amplitude_evaluations"] <= sampler.plan["max_amplitude_evaluations"]
        assert a["decoder_calls"] <= sampler.plan["max_decoder_calls"]
        assert a["pilot_samples"] == a["trials"]


def test_explicit_failure_is_not_silently_renormalized(monkeypatch):
    model, decoder, access = setup(FIXTURES[0])
    sampler = DecodedSampler(model, decoder, access)
    monkeypatch.setattr(old, "bernoulli", lambda probability, rng: False)
    result = sampler.sample(Random(8))
    assert result["status"] == "failure"
    assert result["left"] is result["right"] is result["residue"] is None
    assert result["trials"] == sampler.plan["max_trials"]


def test_mismatched_source_and_fake_oracle_rejected():
    model, decoder, access = setup(FIXTURES[0])
    with pytest.raises(TypeError, match="constructed"):
        DecodedSampler(model, decoder, lambda y: 1)
    changed = d.Physical.create(model.n, model.paulis, [Q(1, 2)]*3, Q(1, 2))
    with pytest.raises(ValueError, match="do not match"):
        DecodedSampler(changed, decoder, access)
    with pytest.raises(ValueError, match="trial budget"):
        DecodedSampler(model, decoder, access, max_trials=1)


def test_median_of_means_budget_and_aggregation(monkeypatch):
    model, decoder, access = setup(FIXTURES[0])
    estimator = PauliEstimator(model, decoder, access, (1, 0, 0))
    plan = estimator.plan(Q(1, 2), Q(1, 4))
    assert plan["block_draws"]*plan["epsilon"]**2 >= 4
    assert plan["blocks"] % 2 == 1
    with pytest.raises(ValueError, match="insufficient draws"):
        estimator.estimate(Random(2), epsilon=Q(1, 2), delta=Q(1, 4), max_draws=10)
    monkeypatch.setattr(estimator, "draw", lambda rng: Q(1, 3))
    result = estimator.estimate(Random(2), epsilon=Q(1, 2), delta=Q(1, 4), max_draws=plan["total_draws"])
    assert result["estimate"] == Q(1, 3)
    assert result["pilot_samples"] == plan["total_draws"]


@pytest.mark.parametrize("delta", [0, 1, -1, .1])
def test_bad_failure_budget(delta):
    model, decoder, access = setup(FIXTURES[0])
    with pytest.raises((ValueError, TypeError)):
        DecodedSampler(model, decoder, access, delta=delta)
