from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
import json
from random import Random

from flint import fq_default_ctx
import pytest

from theorems import native_latent_sampler as module


def test_binomial_endpoints_and_rational_integer_weights():
    assert module.binomial_weights(3, 0) == [1, 0, 0, 0]
    assert module.binomial_weights(3, 1) == [0, 0, 0, 1]
    assert module.binomial_weights(3, Q(1, 3)) == [8, 12, 6, 1]


def test_direct_size_sampler_exhausts_integer_mass_without_rejecting_latent_sets():
    class Ticket:
        def __init__(self, value):
            self.value = value
            self.calls = 0

        def randrange(self, upper):
            assert upper == 26
            self.calls += 1
            return self.value

        def sample(self, population, k):
            return list(population)[:k]

    seen = Counter()
    for ticket in range(26):
        rng = Ticket(ticket)
        seen[len(module.draw_active_set(3, 2, 2, rng))] += 1
        assert rng.calls == 1
    assert seen == {0: 8, 1: 12, 2: 6}
    assert module.draw_active_set(100, 0, 10**50, Random(3)) == ()


def test_exact_conditional_completion_all_random_choices_targets_and_syndromes():
    ctx = fq_default_ctx(2, 2, "z")
    values = [ctx(0), ctx(1), ctx.gen(), ctx.gen()+1]
    pred = [0 if x == 0 else int((x**-1).trace()) for x in values]
    tested = 0
    for active_size in range(3):
        for active in combinations(range(3), active_size):
            pivot = next(i for i in range(3) if i not in active)
            free = [i for i in range(3) if i != pivot]
            widths = [1 if i in active else 2 for i in free]
            for targets in product((0, 1), repeat=3):
                for syndrome in range(4):
                    expected = {word for word in product(range(4), repeat=3)
                                if word[0] ^ word[1] ^ word[2] == syndrome
                                and all(pred[word[i]] == targets[i] for i in active)}
                    draws = []
                    for labels in product(*(range(1 << width) for width in widths)):
                        queue = iter(zip(widths, labels))

                        def bits(width):
                            expected_width, label = next(queue)
                            assert width == expected_width
                            return label

                        word = module.scalar_conditional_draw(ctx, 2, (0, 1, 2), 1,
                                                              targets, (syndrome,), active, bits)
                        assert next(queue, None) is None
                        draws.append(word)
                    assert set(draws) == expected and len(draws) == len(set(draws))
                    tested += 1
    assert tested == 224


def test_second_vandermonde_row_and_nonzero_syndrome_are_not_ignored():
    ctx = fq_default_ctx(2, 3, "z")
    powers = [ctx.gen()**j for j in range(3)]
    elem = lambda x: sum((v for j, v in enumerate(powers) if x >> j & 1), ctx.zero())
    rng = Random(16)
    for targets in product((0, 1), repeat=3):
        word = module.scalar_conditional_draw(ctx, 3, (1, 3, 5), 2, targets, (7, 6), (1,), rng.getrandbits)
        assert sum(map(elem, word), ctx.zero()) == elem(7)
        assert sum((elem(a)*elem(x) for a, x in zip((1, 3, 5), word)), ctx.zero()) == elem(6)


def test_all_finite_mixtures_retain_partition_tilt_empty_fibers_and_native_events():
    saw_nonzero_tv = False
    for targets in product((0, 1), repeat=3):
        for base in (1, Q(3, 2), 10):
            for offset in range(4):
                row = module.finite_audit(2, 3, 1, targets, base, offset)
                assert 0 <= row["tv_exact"] <= row["tv_upper"] <= 1
                saw_nonzero_tv |= row["tv_exact"] > 0
                if base == 1:
                    assert row["tv_exact"] == 0
                if row["ideal_gibbs_native_success"]:
                    assert 0 < row["relative_native_event_capture"] <= 1
    empty = module.finite_audit(2, 3, 2, (1, 1, 1), 10)
    assert empty["native_success"] == 0 and empty["relative_native_event_capture"] is None
    assert saw_nonzero_tv


@pytest.mark.parametrize("remaining,base", [(400, 10), (1200, 3)])
def test_tiny_tv_can_hide_most_native_witness_probability(remaining, base):
    row = module.latent_budget(3200, remaining, base, Q(1, 1 << 100))
    assert row["sampler_tv_upper"] < Q(1, 10**10)
    assert row["relative_native_event_capture_upper"] < Q(1, 10**5)
    assert row["native_success_upper"] <= row["any_feasible_latent_mixture_success_upper"]


def test_search_temperature_has_constant_event_gap_despite_direct_tractable_draw():
    row = module.latent_budget(320, 40, 320, Q(1, 1 << 100))
    assert row["ideal_gibbs_native_success_lower"] > Q(1, 3)
    assert row["native_success_upper"] < Q(1, 1 << 39)
    assert row["retained_proposal_mass"] < Q(1, 10**30)
    active = module.draw_active_set(320, 280, 320, Random(2))
    assert len(active) <= 280
    assert row["direct_truncated_draw_has_rejection_overhead"] is False


@pytest.mark.parametrize("changes", [
    {"active": (0, 1, 2)}, {"active": (1, 1)}, {"active": (True,)},
    {"points": (0, 0, 1)}, {"targets": (True, 0, 0)}, {"syndrome": (4,)},
])
def test_sampler_rejects_unsupported_projection_and_invalid_input(changes):
    args = dict(context=fq_default_ctx(2, 2, "z"), bits=2, points=(0, 1, 2), checks=1,
                targets=(0, 1, 0), syndrome=(0,), active=(1,), draw_bits=Random(0).getrandbits)
    with pytest.raises(ValueError):
        module.scalar_conditional_draw(**(args | changes))


def test_live_artifact_binds_exact_sources_without_promoting_a_full_solver():
    expected = module._jsonable(module.report())
    assert json.loads(module.REPORT.read_text()) == expected
    assert expected["classical_full_search_solved"] is False
    assert expected["quantum_advantage_established"] is False
    assert len(expected["native_certificates"]) == 18
    assert len(expected["finite_controls"]) == 96
