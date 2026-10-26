from itertools import product
import random

import numpy as np
import pytest

from theorems.graded_hsp_phase_descent import (
    UT4Product, controls, coset_fixture, dilation_product_kernel,
    linear_cubic_weights, moment, project_top_center, right_correlations,
)


@pytest.mark.parametrize("p,r", [(5, 1), (11, 2), (17, 3), (65537, 6), (1000000007, 8)])
def test_public_moment_solver_at_growing_rank_and_large_characteristic(p, r):
    rng = random.Random(p+r)
    labels = [[rng.randrange(p) for _ in range(r)] for _ in range((r+1)**2)]
    weights = linear_cubic_weights(p, labels)
    assert any(weights)
    assert not any(moment(labels, weights, 1, p))
    assert not any(moment(labels, weights, 3, p))
    assert linear_cubic_weights(p, labels) == weights


def test_zero_labels_and_extra_inputs_do_not_invalidate_solver():
    labels = [[0, 0]] * 10
    weights = linear_cubic_weights(11, labels)
    assert any(weights)
    assert weights[-1] == 0
    assert moment(labels, weights, 1, 11) == [0, 0]


@pytest.mark.parametrize("p,labels", [
    (7, [[1]]*4), (9, [[1]]*4), (3, [[1]]*4),
    (5, [[1]]*3), (5, []), (5, [[1], [5], [1], [1]]),
])
def test_invalid_or_unsupported_moment_inputs_are_rejected(p, labels):
    with pytest.raises(ValueError):
        linear_cubic_weights(p, labels)


def test_public_kernel_and_moment_interfaces_reject_truncated_or_invalid_weights():
    with pytest.raises(ValueError):
        moment([[1], [2]], [1], 3, 5)
    with pytest.raises(ValueError):
        moment([[1]], [1], 0, 5)
    group = UT4Product(5)
    with pytest.raises(ValueError):
        dilation_product_kernel(group, [{group.identity: 1}], [-1])
    with pytest.raises(ValueError):
        group.power(group.identity, -1)


def test_actual_class_three_group_and_public_dilation_identities():
    group = UT4Product(11, 2)
    rng = random.Random(191)
    for _ in range(30):
        a, b, c = [tuple(rng.randrange(group.p) for _ in group.identity) for _ in range(3)]
        assert group.multiply(group.multiply(a, b), c) == group.multiply(a, group.multiply(b, c))
        assert group.multiply(a, group.inverse(a)) == group.identity
        for scale in (1, 2, 10):
            assert group.dilate(group.multiply(a, b), scale) == group.multiply(
                group.dilate(a, scale), group.dilate(b, scale))
            assert group.dilate(group.dilate(a, scale), pow(scale, -1, group.p)) == a
        assert group.power(a, group.p) == group.identity
    with pytest.raises(ValueError):
        group.dilate(a, 0)


def test_logarithmic_grade_promise_is_not_a_zero_matrix_entry_promise():
    group = UT4Product(11)
    h = group.exp([1, 2, 3, 0, 0, 4])
    assert h[3] != 0 and h[4] != 0
    for scale in range(1, group.p):
        delta = group.multiply(group.dilate(h, scale), group.inverse(group.power(h, scale)))
        assert delta == group.center([(scale**3-scale)*4 % group.p])
    broken = group.exp([1, 2, 3, 1, 0, 4])
    delta = group.multiply(group.dilate(broken, 2), group.inverse(group.power(broken, 2)))
    assert delta[3] != 0


def test_central_fourier_projection_is_complete_and_independent_of_coset():
    group = UT4Product(5)
    h = group.exp([1, 2, 1, 0, 0, 3])
    representatives = [group.identity, (1, 2, 3, 4, 0, 1)]
    kernels, total = [], 0
    for u in range(group.p):
        pair = []
        for a in representatives:
            state, probability = project_top_center(group, coset_fixture(group, h, a), [u])
            assert probability == pytest.approx(1/group.p, abs=1e-12)
            pair.append(right_correlations(group, state))
        assert pair[0].keys() == pair[1].keys()
        assert max(abs(pair[0][g]-pair[1][g]) for g in pair[0]) < 1e-12
        total += probability
        kernels.append(pair[0])
        for z in range(group.p):
            assert pair[0][group.center([z])] == pytest.approx(np.exp(2j*np.pi*u*z/group.p))
    assert total == pytest.approx(1.0)


def test_dilation_kernel_agrees_with_direct_controlled_action():
    group = UT4Product(5)
    h = group.exp([1, 2, 1, 0, 0, 3])
    labels = [[1], [2], [3], [4]]
    weights = linear_cubic_weights(group.p, labels)
    states = [project_top_center(group, coset_fixture(group, h, group.identity), u)[0]
              for u in labels]
    kernels = [right_correlations(group, state) for state in states]
    combined = dilation_product_kernel(group, kernels, weights)
    # Check all group coordinates, not just proposed subgroup generators.
    for g in product(range(group.p), repeat=6):
        actual = 1+0j
        for state, scale in zip(states, weights):
            if not scale:
                continue
            shift = group.inverse(group.dilate(g, scale))
            actual *= sum(np.conjugate(state.get(group.multiply(x, shift), 0j))*a
                          for x, a in state.items())
        assert abs(actual-combined.get(g, 0j)) < 1e-11


def test_vector_center_conversion_uses_one_common_hidden_parameter():
    group = UT4Product(5, 2)
    h = group.exp([1, 2, 1, 0, 0, 3, 2, 1, 3, 0, 0, 4])
    rng = random.Random(277)
    labels = [[rng.randrange(5), rng.randrange(5)] for _ in range(9)]
    weights = linear_cubic_weights(5, labels)
    kernels = []
    for label in labels:
        representative = tuple(rng.randrange(5) for _ in group.identity)
        state, probability = project_top_center(
            group, coset_fixture(group, h, representative), label)
        assert probability == pytest.approx(1/25)
        kernels.append(right_correlations(group, state))
    output = dilation_product_kernel(group, kernels, weights)
    expected = {group.multiply(group.power(h, t), group.center(z))
                for t in range(5) for z in product(range(5), repeat=2)}
    assert len(expected) == 125
    assert output.keys() == expected
    assert max(abs(value-1) for value in output.values()) < 1e-11


def test_promised_conversion_and_both_scope_falsifiers():
    report = controls()
    assert report["gram_control"]["maximum_error"] < 1e-10
    assert report["gram_control"]["computed_support"] == 121
    assert report["cubic_only_negative"]["cubic_moment"] == [0]
    assert report["cubic_only_negative"]["linear_moment"] != [0]
    assert report["cubic_only_negative"]["error_from_required_one"] > 0.1
    assert report["grade_two_negative"]["error_from_required_HZ"] > 0.9
    assert report["grade_two_negative"]["error_from_center_only"] < 1e-10
    assert report["grade_two_negative"]["hidden_generator_overlap_abs"] < 1e-12
    assert report["all_moments_negative"]["moments_one_through_three"] == [[0], [0], [0]]
    assert report["all_moments_negative"]["error_from_center_only"] < 1e-10
    assert report["all_moments_negative"]["error_from_required_HZ"] > 0.9
    assert report["common_scaling_positive"]["error_from_publicly_rescaled_HZ"] < 1e-10
    assert report["common_scaling_positive"]["error_from_unrescaled_HZ"] > 0.9
    assert report["scope"]["entire_promised_HSP_receiver_executed"] is False
    assert report["scope"]["novelty_established"] is False
