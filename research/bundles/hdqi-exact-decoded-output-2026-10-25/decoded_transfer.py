"""Exact actual decoded-output sampling and complex Pauli importance weights.

All results target the specified finite transfer pilot and actual decoder.
Neither a Gibbs guarantee nor small interference rank is inferred.
"""

from fractions import Fraction as Q
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"hdqi-output-sampling-2026-10-24"))
import output_sampling as old
from transfer_access import TransferAccess, conjugate, fraction, gaussian
from tree_sampler import rational

d = old.d


def unit_phase(exponent):
    return (gaussian(1), gaussian((0, 1)), gaussian(-1), gaussian((0, -1)))[exponent % 4]


def squared(value):
    result = value*conjugate(value)
    if result.y or result.x < 0:
        raise ArithmeticError("invalid exact squared modulus")
    return fraction(result.x)


def checked_pair(model, access):
    if not isinstance(access, TransferAccess):
        raise TypeError("constructed TransferAccess required, not an amplitude callback")
    rebuilt = d.Physical.create(model.n, model.paulis, model.pilot.couplings, model.pilot.beta)
    if rebuilt != model:
        raise ValueError("physical model does not match its own canonical pilot")
    if (model.pilot.m != access.m or model.pilot.edges != access.decomposition.edges
            or model.pilot.couplings != access.couplings):
        raise ValueError("physical input and transfer pilot do not match")


def rounds_for(delta):
    delta = rational(delta)
    if not 0 < delta < 1:
        raise ValueError("failure probability must lie strictly between zero and one")
    rounds = 0
    while Q(1, 1 << rounds) > delta:
        rounds += 1
    return delta, rounds


class DecodedSampler:
    def __init__(self, model, decoder, access, *, delta=Q(1, 16),
                 max_fiber=4096, max_trials=1_000_000):
        checked_pair(model, access)
        self.model, self.decoder, self.access = model, decoder, access
        ranks = old.pure_z_basis(model)
        delta, rounds = rounds_for(delta)
        bound = ranks["fiber_bound"]
        if type(max_fiber) is not int or max_fiber < bound:
            raise ValueError("interference fiber exceeds explicit budget, not a hardness result")
        if type(max_trials) is not int or max_trials < bound*rounds:
            raise ValueError("trial budget insufficient for stated failure probability")
        self.plan = {**ranks, "delta": delta, "max_trials": bound*rounds,
                     "success_probability_per_trial": Q(1, bound),
                     "failure_probability_upper": Q(1, 1 << rounds),
                     "max_pilot_samples": bound*rounds,
                     "max_amplitude_evaluations": bound*bound*rounds,
                     "max_decoder_calls": (bound+1)*bound*rounds,
                     "average_sign_bound_required": False,
                     "decoder_total_deterministic_required": True,
                     "decoder_runtime_certified": False,
                     "pilot_thermal_accuracy_certified": False,
                     "gibbs_accuracy_certified": False,
                     "target": "actual_decoded_joint_computational_output_of_transfer_pilot"}
        self.max_fiber = max_fiber

    def proposal(self, representative, right):
        if type(right) is not int or not 0 <= right < 1 << self.model.n:
            raise ValueError("right output must be an n-bit word")
        residue, labels = old.fiber(self.model, self.decoder, representative,
                                   self.plan["z_basis"], self.max_fiber)
        mass, coherent = Q(0), gaussian(0)
        for y in labels:
            amplitude = self.access.amplitude(y)
            mass += squared(amplitude)
            _, z, phase = self.model.ordered(y)
            # Coupling signs are ALREADY in the exact pilot amplitudes.
            coherent += amplitude*unit_phase(phase+2*(z & right).bit_count())
        if not mass:
            raise ValueError("zero-probability proposal fiber")
        acceptance = squared(coherent)/(self.plan["fiber_bound"]*mass)
        if not 0 <= acceptance <= 1:
            raise ArithmeticError("exact interference envelope failed")
        x = self.model.label(representative) & ((1 << self.model.n)-1)
        return {"residue": residue, "left": right ^ x, "right": right,
                "fiber_mass": mass, "coherent_square": squared(coherent),
                "acceptance": acceptance, "fiber_size": len(labels)}

    def sample(self, rng):
        amplitude_calls = 0
        for trial in range(1, self.plan["max_trials"]+1):
            representative = self.access.sample(rng)
            record = self.proposal(representative, rng.getrandbits(self.model.n))
            amplitude_calls += record["fiber_size"]
            if old.bernoulli(record["acceptance"], rng):
                return {"status": "sample", **{k: record[k] for k in ("residue", "left", "right")},
                        "trials": trial, "pilot_samples": trial,
                        "amplitude_evaluations": amplitude_calls,
                        "decoder_calls": trial*(self.plan["fiber_bound"]+1)}
        return {"status": "failure", "residue": None, "left": None, "right": None,
                "trials": self.plan["max_trials"], "pilot_samples": self.plan["max_trials"],
                "amplitude_evaluations": amplitude_calls,
                "decoder_calls": self.plan["max_trials"]*(self.plan["fiber_bound"]+1)}


def complex_partner(model, decoder, observable, y):
    d.validate_pauli(model.n, observable)
    if type(y) is not int or not 0 <= y < 1 << model.pilot.m:
        raise ValueError("invalid native word")
    syndrome = model.label(y)
    target = syndrome ^ observable[0] ^ (observable[1] << model.n)
    other = y ^ old.decoder_value(model, decoder, syndrome) ^ old.decoder_value(model, decoder, target)
    if model.label(other) != target:
        return None
    x, z, phase = d.multiply(d.dagger(model.ordered(other)), d.multiply(observable, model.ordered(y)))
    if x or z:
        raise ArithmeticError("partner product must be scalar")
    return other, unit_phase(phase)


class PauliEstimator:
    def __init__(self, model, decoder, access, observable):
        checked_pair(model, access)
        d.validate_pauli(model.n, observable)
        self.model, self.decoder, self.access, self.observable = model, decoder, access, observable

    def value(self, y):
        a = self.access.amplitude(y)
        if not a:
            raise ValueError("importance value requested at zero source probability")
        other = complex_partner(self.model, self.decoder, self.observable, y)
        if other is None:
            return Q(0)
        t, phase = other
        # Re(omega*conj(a_t)/conj(a_y)); taking Re(omega) first is wrong for complex pilots.
        weight = phase*conjugate(self.access.amplitude(t))/conjugate(a)
        return fraction(weight.x)

    def draw(self, rng):
        return self.value(self.access.sample(rng))

    def plan(self, epsilon=Q(1, 8), delta=Q(1, 16)):
        epsilon = rational(epsilon)
        delta, rounds = rounds_for(delta)
        if not 0 < epsilon <= 1:
            raise ValueError("need 0<epsilon<=1")
        block = old.s.ceil_fraction(4/epsilon**2)
        groups = 8*rounds+1
        return {"epsilon": epsilon, "delta": delta, "block_draws": block,
                "blocks": groups, "total_draws": block*groups,
                "second_moment_upper": Q(1), "max_amplitude_evaluations": 2*block*groups,
                "max_decoder_calls": 2*block*groups, "average_sign_bound_required": False,
                "fiber_enumeration_required": False, "gibbs_accuracy_certified": False,
                "decoder_total_deterministic_required": True,
                "decoder_runtime_certified": False, "pilot_thermal_accuracy_certified": False}

    def estimate(self, rng, *, epsilon=Q(1, 8), delta=Q(1, 16), max_draws=1_000_000):
        plan = self.plan(epsilon, delta)
        if type(max_draws) is not int or max_draws < plan["total_draws"]:
            raise ValueError("insufficient draws; no certified estimate produced")
        means = [sum((self.draw(rng) for _ in range(plan["block_draws"])), Q(0))/plan["block_draws"]
                 for _ in range(plan["blocks"])]
        estimate = max(Q(-1), min(Q(1), statistics.median(means)))
        return {"status": "estimate", "estimate": estimate, "plan": plan,
                "pilot_samples": plan["total_draws"]}
