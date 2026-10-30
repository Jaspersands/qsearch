from fractions import Fraction as F
from itertools import product
import math
import random

import numpy as np
import pytest

import interference_distance as d


@pytest.mark.parametrize("beta", [F(0), F(1, 16), F(1, 4), F(1)])
@pytest.mark.parametrize("decoder_kind", ["nonlinear", "zero", "random"])
def test_full_physical_output_including_nonlinear_and_bad_decoders(beta, decoder_kind):
    model, decoder = d.nonlinear_fixture(beta)
    if decoder_kind == "zero":
        decoder = lambda syndrome: 0
    if decoder_kind == "random":
        rng = random.Random(99)
        table = [rng.randrange(16) for _ in range(16)]
        decoder = table.__getitem__
    result = d.dense_control(model, decoder, 1)
    assert result["truncated_uniform_max_error"] < 1e-12
    assert result["actual_left_TV"]**2 <= result["actual_tail"]+1e-12


def test_proper_decoder_is_genuinely_nonlinear_on_reachable_syndromes():
    model, decoder = d.nonlinear_fixture()
    image = {model.label(y) for y in range(16)}
    assert all(model.label(decoder(s)) == s for s in image)
    assert any(decoder(a ^ b) != decoder(a) ^ decoder(b) for a in image for b in image)


def test_thermal_control_has_nonzero_bias_before_projection():
    model, decoder = d.nonlinear_fixture(F(1))
    result = d.dense_control(model, decoder, 1)
    assert result["actual_left_TV"] > .01
    assert result["truncated_uniform_max_error"] < 1e-12


def test_relative_distance_ignores_scalar_products_but_detects_diagonal_ones():
    model, _ = d.nonlinear_fixture()
    assert model.label(9) == 0 and (9).bit_count() == 2
    assert d.low_weight_check(model, 1)["status"] == "CERTIFIED"
    bad = d.low_weight_check(model, 2)
    assert bad["status"] == "SHORT_DIAGONAL_WORD"
    assert bad["witness"]["weight"] == 3
    assert model.label(bad["witness"]["mask"]) == bad["witness"]["Z"] << model.n


def test_arbitrary_complex_amplitudes_in_good_subspace_give_uniform_left():
    model, decoder = d.nonlinear_fixture()
    rng = np.random.default_rng(38)
    for _ in range(8):
        psi = rng.normal(size=16)+1j*rng.normal(size=16)
        psi[[y for y in range(16) if y.bit_count() > 1]] = 0
        psi /= np.linalg.norm(psi)
        left = d.left_marginal(d.dense_joint(model, decoder, psi), 2)
        assert np.max(abs(left-.25)) < 1e-12


def test_short_diagonal_word_is_a_real_opposite_control_not_automatic_hardness():
    model = d.o.d.Physical.create(1, [(0, 1, 0)], [1], 1)
    assert d.low_weight_check(model, 1)["status"] == "SHORT_DIAGONAL_WORD"
    psi = d.dense_pilot(model)
    left = d.left_marginal(d.dense_joint(model, lambda s: s >> 1, psi), 1)
    assert abs(left[0]-.5) > .3
    plan = d.certify(model, 1)
    assert plan["status"] == "NO_CERTIFICATE" and plan["TV_squared_upper"] is None
    assert not plan["hardness_from_refusal"]


def test_factorial_bound_against_exact_inhomogeneous_bernoulli_tail():
    model = d.o.d.Physical.create(2, [(1, 0, 0), (2, 0, 0), (3, 0, 0)], [1, F(1, 2), 0], F(1, 2))
    rhos = [x*x for x in model.pilot.x]
    for t in range(4):
        exact = sum(math.prod(rhos[i] if bit else 1-rhos[i] for i, bit in enumerate(bits))
                    for bits in product((0, 1), repeat=3) if sum(bits) > t)
        assert exact <= d.factorial_tail(model, t)["tail_upper"]
    assert d.factorial_tail(model, 3)["tail_upper"] == 0


def test_sparse_failure_budget_not_promoted_to_a_distance_certificate():
    model = d.scrambled_pairs(8)
    row = d.low_weight_check(model, 2, max_vectors=0)
    assert row["status"] == "UNKNOWN_BUDGET" and row["checked_vectors"] == 0
    assert not row["no_short_relative_word"]
    with pytest.raises(ValueError, match="no certified sampler"):
        d.UniformSampler(model, 2, max_vectors=0)


def test_large_rank_public_fixture_certifies_without_fiber_or_state_enumeration():
    model = d.scrambled_pairs()
    sampler = d.UniformSampler(model, 2, F(1, 1000))
    assert sampler.plan["fiber_ranks"]["fiber_rank"] == 32
    assert sampler.plan["fiber_ranks"]["fiber_bound"] == 2**32
    with pytest.raises(d.o.s.BudgetExceeded, match="fiber"):
        d.o.Sampler(model, lambda syndrome: 0)
    assert sampler.plan["distance_check"]["checked_vectors"] == sum(math.comb(64, k) for k in range(1, 5))
    assert F(sampler.plan["tail_upper"]) < F(1, 1000000)
    rng = random.Random(24)
    assert all(0 <= sampler.sample(rng) < 2**32 for _ in range(10))
    with pytest.raises(ValueError, match="dense reference"):
        d.dense_pilot(model)


def test_joint_output_is_not_claimed_to_be_uniform():
    model = d.o.d.Physical.create(1, [(1, 0, 0)], [1], 0)
    joint = d.dense_joint(model, lambda s: s, d.dense_pilot(model))
    assert sum(p for (_, a, b), p in joint.items() if a == b) == pytest.approx(1)
    assert np.allclose(d.left_marginal(joint, 1), [.5, .5])


def test_square_root_tail_loss_cannot_be_replaced_by_tail_mass():
    model = d.o.d.Physical.create(1, [(0, 1, 0)], [1], 0)
    eta = .01
    psi = np.array([math.sqrt(1-eta), math.sqrt(eta)])
    left = d.left_marginal(d.dense_joint(model, lambda s: s >> 1, psi), 1)
    tv = float(np.sum(abs(left-.5))/2)
    assert tv == pytest.approx(math.sqrt(eta*(1-eta)))
    assert tv > eta


def test_distance_must_be_strictly_greater_than_twice_the_cutoff():
    model = d.o.d.Physical.create(1, [(1, 0, 0), (1, 1, 1)], [1, 1], 0)
    section = {model.label(y): y for y in range(4)}
    psi = np.array([0, 1, 1j, 0])/math.sqrt(2)
    left = d.left_marginal(d.dense_joint(model, section.__getitem__, psi), 1)
    assert abs(left[0]-.5) == pytest.approx(.5)
    check = d.low_weight_check(model, 1)
    assert check["status"] == "SHORT_DIAGONAL_WORD" and check["witness"]["weight"] == 2


@pytest.mark.parametrize("t,budget", [(-1, 10), (True, 10), (5, 10), (1, -1)])
def test_invalid_certificate_inputs(t, budget):
    model, _ = d.nonlinear_fixture()
    with pytest.raises(ValueError):
        d.low_weight_check(model, t, budget)


def test_requested_accuracy_and_normalization_are_enforced():
    model, decoder = d.nonlinear_fixture()
    with pytest.raises(ValueError):
        d.UniformSampler(model, 1, F(1, 1000000))
    with pytest.raises(ValueError):
        d.certify(model, 1, 0)
    with pytest.raises(ValueError):
        d.dense_joint(model, decoder, np.zeros(16))
