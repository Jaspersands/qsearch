from fractions import Fraction as F
from itertools import product
import math
import random

import numpy as np
import pytest
from scipy.linalg import expm

import output_sampling as o


def matrix(pauli, n):
    x, z, phase = pauli
    out = np.zeros((1 << n, 1 << n), dtype=complex)
    for b in range(1 << n):
        out[b ^ x, b] = (1j)**phase * (-1)**(z & b).bit_count()
    return out


def exact_physical_law(model, decoder):
    m = model.pilot.m
    h = np.zeros((1 << m, 1 << m))
    for i, j in enumerate(model.pilot.couplings):
        h += float(j)*matrix((1 << i, model.pilot.lower_masks[i], 0), m).real
    pilot = expm(-float(model.pilot.beta)*h/2)[:, 0]
    pilot /= np.linalg.norm(pilot)
    sectors = {}
    for y, amplitude in enumerate(pilot):
        p = np.eye(1 << model.n, dtype=complex)
        for i, generator in enumerate(model.paulis):
            if y >> i & 1:
                p = p @ matrix(generator, model.n)
        residue = y ^ decoder(model.label(y))
        sectors[residue] = sectors.get(residue, np.zeros_like(p))+amplitude*p/math.sqrt(1 << model.n)
    return {(residue, a, b): abs(p[a, b])**2 for residue, p in sectors.items()
            for a in range(1 << model.n) for b in range(1 << model.n)}


@pytest.mark.parametrize("paulis", (((1, 0, 0), (0, 1, 0)),
                                    ((1, 0, 0), (1, 0, 0), (0, 1, 0)),
                                    ((0, 1, 0), (0, 2, 0), (0, 3, 0)),
                                    ((1, 0, 0), (0, 3, 0), (3, 1, 1))))
def test_rank_and_all_fibers_match_bruteforce_not_decoder_inversion(paulis):
    model = o.d.Physical.create(2, paulis, [1]*len(paulis), F(1, 4))
    info = o.pure_z_basis(model)
    images = {model.label(y) for y in range(1 << len(paulis))}
    xs = {syndrome & 3 for syndrome in images}
    assert len(images) == 1 << info["rank_B"]
    assert len(xs) == 1 << info["rank_X"]
    assert len([s for s in images if not s & 3]) == info["fiber_bound"]
    rng = random.Random(32)
    for _ in range(8):
        table = [rng.randrange(1 << len(paulis)) for _ in range(16)]
        decoder = table.__getitem__
        for y0 in range(1 << len(paulis)):
            residue, values = o.fiber(model, decoder, y0, info["z_basis"], info["fiber_bound"])
            expected = tuple(y for y in range(1 << len(paulis))
                             if (model.label(y) & 3) == (model.label(y0) & 3)
                             and y ^ decoder(model.label(y)) == residue)
            assert values == expected


@pytest.mark.parametrize("paulis", (((1, 0, 0), (1, 0, 0), (0, 1, 0)),
                                    ((1, 0, 0), (0, 1, 0), (1, 1, 1)),
                                    ((0, 1, 0), (0, 2, 0), (0, 3, 0))))
@pytest.mark.parametrize("bad_decoder", (False, True))
def test_entire_accepted_law_has_exact_mixture_and_matches_actual_output(paulis, bad_decoder):
    model = o.d.Physical.create(2, paulis, [1, F(-1, 2), F(3, 4)], F(1, 4))
    table = {model.label(y): y for y in reversed(range(8))}
    decoder = (lambda syndrome: 0) if bad_decoder else (lambda syndrome: table.get(syndrome, 0))
    sampler = o.Sampler(model, decoder)
    law = o.finite_law(sampler)
    assert sum(law["accepted"].values()) == 1
    assert sum(law["target"].values()) == 1
    assert sum(law["envelope"].values()) == 1
    for event, probability in law["accepted"].items():
        assert probability == (1-law["alpha"])*law["target"][event]+law["alpha"]*law["envelope"][event]
    assert law["alpha"] <= sampler.plan["mixture_bias_upper"] <= sampler.plan["epsilon"]/4
    assert law["success"] >= sampler.plan["success_probability_lower"]
    actual = exact_physical_law(model, decoder)
    tv = sum(abs(float(law["accepted"].get(event, 0))-actual.get(event, 0))
             for event in set(actual) | set(law["accepted"]))/2
    assert tv <= float(sampler.plan["epsilon"])/2


def test_bell_pushforward_is_not_the_computational_output_distribution():
    model = o.d.Physical.create(1, [(0, 1, 0)], [1], 1)
    sampler = o.Sampler(model, lambda syndrome: syndrome >> 1)
    law = o.finite_law(sampler)
    p0 = sum(p for (_, left, _), p in law["accepted"].items() if left == 0)
    thermal = math.exp(-1)/(2*math.cosh(1))
    assert abs(float(p0)-thermal) < float(sampler.plan["epsilon"])/2
    assert abs(p0-F(1, 2)) > F(1, 4)


def test_complex_phase_second_moment_identity_is_not_real_sign_squaring():
    values = ((1, 0), (0, 1), (-1, 0), (0, -1))
    probabilities = (F(1, 2), F(1, 4), F(1, 8), F(1, 8))
    k = 3
    expected = F(0)
    for indices in product(range(4), repeat=k):
        real = sum(values[i][0] for i in indices)
        imag = sum(values[i][1] for i in indices)
        expected += math.prod(probabilities[i] for i in indices)*F(real*real+imag*imag, k*k)
    mean_square = sum(p*v[0] for p, v in zip(probabilities, values))**2+sum(p*v[1] for p, v in zip(probabilities, values))**2
    assert expected == mean_square+(1-mean_square)/k


def test_zero_probability_fiber_entries_never_request_odd_words():
    model = o.d.Physical.create(1, [(1, 0, 0), (0, 1, 0)], [1, 0], F(1, 4))
    sampler = o.Sampler(model, lambda syndrome: syndrome)
    _, law, acceptance = sampler.fiber_law(0)
    assert acceptance <= 1
    assert dict(law.probabilities())[2] == 0
    for _ in range(8):
        assert sampler.sample(random.Random(_))["status"] == "sample"


def test_large_fiber_refusal_is_not_a_hardness_certificate():
    n = 30
    model = o.d.Physical.create(n, [(0, 1 << i, 0) for i in range(n)], [1]*n, F(1, 4))
    p = o.plan(model)
    assert p["fiber_rank"] == n and p["ratio_upper"] == 1
    with pytest.raises(o.s.BudgetExceeded, match="fiber"):
        o.Sampler(model, lambda syndrome: syndrome >> n, max_fiber=8)
    # This refused input is an easy product thermal law, not a hard family.
    thermal_one = math.exp(0.25)/(2*math.cosh(0.25))
    assert 0 < thermal_one < 1


def test_live_nontrivial_fiber_is_reproducible_and_resource_bounded():
    model, decoder = o.large_fixture(12)
    sampler = o.Sampler(model, decoder)
    assert sampler.plan["fiber_rank"] == 1
    left, right = random.Random(42), random.Random(42)
    for _ in range(8):
        a, b = sampler.sample(left), sampler.sample(right)
        assert a == b
        assert a["status"] == "sample"
        assert 0 <= a["left"] < 1 << 12 and 0 <= a["right"] < 1 << 12
        assert a["residue"] == 0
        assert a["words"] <= sampler.plan["max_words"]
        assert a["letters"] <= a["words"]*sampler.plan["max_word_letters"]
        assert a["decoder_calls"] <= sampler.plan["max_decoder_calls"]


def test_rejected_proposals_do_not_fabricate_an_output(monkeypatch):
    model = o.d.Physical.create(1, [(0, 1, 0)], [1], F(1, 4))
    sampler = o.Sampler(model, lambda syndrome: syndrome >> 1)
    monkeypatch.setattr(o, "bernoulli", lambda probability, rng: False)
    out = sampler.sample(random.Random(4))
    assert out["status"] == "failure"
    assert out["left"] is out["right"] is out["residue"] is None
    assert out["words"] == 0
    assert out["trials"] == sampler.plan["max_trials"]


def test_work_budget_and_dense_reference_caps_are_explicit():
    model, decoder = o.large_fixture(12)
    with pytest.raises(o.s.BudgetExceeded, match="word budget"):
        o.Sampler(model, decoder, max_word_budget=1)
    with pytest.raises(ValueError, match="finite law"):
        o.finite_law(o.Sampler(model, decoder))

