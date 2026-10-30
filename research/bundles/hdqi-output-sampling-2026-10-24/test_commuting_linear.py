from collections import Counter
from fractions import Fraction as F
from itertools import product
import math
import random

import pytest

import commuting_linear as l
import output_sampling as o
from test_output_sampling import exact_physical_law


def finite_left_law(sampler):
    model = sampler.model
    out = [F(0)]*(1 << model.n)
    for word in range(1 << model.pilot.m):
        probability = math.prod(law.probabilities()[word >> i & 1][1] for i, law in enumerate(sampler.coins))
        rhs = [phase ^ ((h & word).bit_count() % 2) for phase, h in zip(sampler.phases, sampler.h)]
        solutions = [x for x in range(1 << model.n)
                     if all((z & x).bit_count() % 2 == b for z, b in zip(sampler.constraints, rhs))]
        for x in solutions:
            out[x] += probability/len(solutions)
    return out


@pytest.mark.parametrize("paulis", (((0, 1, 0), (0, 2, 0), (0, 3, 2)),
                                    ((3, 0, 0), (0, 3, 0), (3, 3, 0)),
                                    ((1, 0, 0), (2, 0, 0), (3, 0, 2)),
                                    ((1, 1, 1), (2, 2, 1), (3, 3, 2))))
def test_all_left_probabilities_match_actual_output_with_relations_and_phases(paulis):
    model = o.d.Physical.create(2, paulis, [1, F(-1, 2), F(3, 4)], F(1, 2))
    decoder = l.build_linear_decoder(model)
    sampler = l.Sampler(model, decoder)
    actual_joint = exact_physical_law(model, decoder)
    actual = [sum(p for (_, left, _), p in actual_joint.items() if left == x) for x in range(4)]
    output = finite_left_law(sampler)
    assert sum(output) == 1
    assert sum(abs(float(a)-b) for a, b in zip(output, actual))/2 <= float(sampler.epsilon)
    for a, b in product(range(16), repeat=2):
        assert decoder(a ^ b) == decoder(a) ^ decoder(b)
    for y in range(8):
        assert model.label(decoder(model.label(y))) == model.label(y)


def test_uniform_affine_solver_enumerates_each_solution_equally():
    class Bits:
        def __init__(self, word):
            self.word, self.offset = word, 0

        def getrandbits(self, count):
            value = (self.word >> self.offset) & ((1 << count)-1)
            self.offset += count
            return value

    # Two independent constraints leave two free bits.
    counts = Counter(l.affine_solution(4, (0b0101, 0b1010), (1, 0), Bits(word)) for word in range(4))
    assert len(counts) == 4 and set(counts.values()) == {1}
    for x in counts:
        assert (x & 0b0101).bit_count() % 2 == 1
        assert (x & 0b1010).bit_count() % 2 == 0
    with pytest.raises(ValueError, match="inconsistent"):
        l.affine_solution(2, (1, 1), (0, 1), Bits(0))


def test_high_rank_input_refused_by_generic_sampler_is_sampled_without_enumeration():
    n = 128
    model = o.d.Physical.create(n, [(0, 1 << i, 0) for i in range(n)], [1]*n, F(1, 2))
    decoder = l.build_linear_decoder(model)
    sampler = l.Sampler(model, decoder)
    assert sampler.ledger()["diagonal_rank"] == 128
    assert not sampler.ledger()["fiber_enumeration_used"]
    for seed in range(8):
        a, b = sampler.sample(random.Random(seed)), sampler.sample(random.Random(seed))
        assert a == b and 0 <= a < 1 << n


def test_shortcut_rejects_noncommuting_nonlinear_and_nonsection_inputs():
    model = o.d.Physical.create(1, [(1, 0, 0), (0, 1, 0)], [1, 1], F(1, 4))
    with pytest.raises(ValueError, match="commuting"):
        l.Sampler(model, l.build_linear_decoder(model))
    diagonal = o.d.Physical.create(1, [(0, 1, 0)], [1], F(1, 4))
    with pytest.raises(ValueError, match="explicit verified linear"):
        l.Sampler(diagonal, lambda syndrome: syndrome >> 1)
    with pytest.raises(ValueError, match="BDB"):
        l.LinearDecoder.create(diagonal, (0, 0))


def test_zero_and_signed_biases_have_the_correct_temperature_convention():
    model = o.d.Physical.create(2, [(0, 1, 0), (0, 2, 0)], [0, -1], F(1, 2))
    sampler = l.Sampler(model, l.build_linear_decoder(model))
    assert sampler.biases[0] == 0
    assert sampler.biases[1] > 0
    assert abs(float(sampler.biases[1])-math.tanh(0.5)) <= float(9*sampler.eta)


def test_valid_linear_section_can_still_give_the_wrong_gibbs_state():
    model = o.d.Physical.create(1, [(0, 1, 0), (0, 0, 0)], [1, 1], F(1, 2))
    decoder = l.LinearDecoder.create(model, (0, 3))
    sampler = l.Sampler(model, decoder)
    output = finite_left_law(sampler)
    actual_joint = exact_physical_law(model, decoder)
    actual_zero = sum(p for (_, left, _), p in actual_joint.items() if left == 0)
    assert abs(float(output[0])-actual_zero) < float(sampler.epsilon)
    mean = float(output[0]-output[1])
    assert abs(mean-math.tanh(0.5)**2) < float(sampler.epsilon)
    intended_gibbs_mean = -math.tanh(0.5)
    assert abs(mean-intended_gibbs_mean) > 0.5
