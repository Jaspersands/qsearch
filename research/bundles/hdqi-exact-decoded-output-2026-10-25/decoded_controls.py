"""Bounded exact physical-state references. Never an input to the sampler."""

from fractions import Fraction as Q

from decoded_transfer import squared, unit_phase
from transfer_access import conjugate, fraction, gaussian
from tree_controls import direct_native_vector


def direct_state(model, decoder, parameters):
    if model.n > 4 or model.pilot.m > 8:
        raise ValueError("exponential physical reference capped at n<=4,m<=8")
    pilot = direct_native_vector(model.pilot.couplings, model.pilot.edges, parameters)
    state = {}
    for y, amplitude in enumerate(pilot):
        residue = y ^ decoder(model.label(y))
        for right in range(1 << model.n):
            left, value = right, amplitude
            # Direct generator action, not the production ordered-product phase.
            for i in reversed(range(model.pilot.m)):
                if y >> i & 1:
                    x, z, phase = model.paulis[i]
                    value *= unit_phase(phase+2*(z & left).bit_count())
                    left ^= x
            key = (residue, left, right)
            state[key] = state.get(key, gaussian(0))+value
    norm = sum(map(squared, state.values()), Q(0))
    expected = (1 << model.n)*sum(map(squared, pilot), Q(0))
    if norm != expected:
        raise AssertionError("actual decoder map failed exact isometry")
    return state, norm


def output_law(model, decoder, parameters):
    state, norm = direct_state(model, decoder, parameters)
    return {event: squared(value)/norm for event, value in state.items()}


def observable_mean(model, decoder, parameters, observable):
    state, norm = direct_state(model, decoder, parameters)
    x, z, phase = observable
    mean = gaussian(0)
    for (residue, left, right), amplitude in state.items():
        partner = state.get((residue, left ^ x, right), gaussian(0))
        mean += conjugate(partner)*amplitude*unit_phase(phase+2*(z & left).bit_count())
    if mean.y:
        raise AssertionError("nonreal Hermitian observable expectation")
    return fraction(mean.x)/norm


def accepted_trial_law(sampler):
    model = sampler.model
    if model.n > 4 or model.pilot.m > 8:
        raise ValueError("exhaustive trial law capped at n<=4,m<=8")
    law = {}
    for y in range(1 << model.pilot.m):
        probability = sampler.access.probability(y)
        if not probability:
            continue
        for right in range(1 << model.n):
            record = sampler.proposal(y, right)
            event = tuple(record[key] for key in ("residue", "left", "right"))
            law[event] = law.get(event, Q(0))+probability*record["acceptance"]/(1 << model.n)
    return law


def exact_importance_moments(estimator):
    if estimator.access.m > 8:
        raise ValueError("exhaustive importance moments capped at eight generators")
    mean, second = Q(0), Q(0)
    for y in range(1 << estimator.access.m):
        probability = estimator.access.probability(y)
        if probability:
            value = estimator.value(y)
            mean += probability*value
            second += probability*value**2
    return mean, second
