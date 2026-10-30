from fractions import Fraction
from itertools import product

import numpy as np
import pytest

from correlated_source import ReesHeisenberg, acquisition_bound, evaluate_character


@pytest.mark.parametrize("p", [3, 5, 7])
def test_group_and_actual_hidden_lines(p):
    group = ReesHeisenberg(p)
    x, y, z = (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1)
    assert group.mul(group.mul(x, y), group.mul(group.inv(x), group.inv(y))) == z
    for axis in ("X", "Y"):
        hidden = set(group.hidden(axis))
        assert all(group.mul(a, b) in hidden for a, b in product(hidden, repeat=2))
        assert hidden.intersection({(0, 0, 0, t) for t in range(p)}) == {group.identity}
    assert group.conjugate(y, x) not in group.hidden("X")
    for a in group.elements:
        assert group.mul(a, group.inv(a)) == group.identity
        assert group.mul(group.mul(a, x), y) == group.mul(a, group.mul(x, y))


@pytest.mark.parametrize("p", [3, 5])
@pytest.mark.parametrize("axis", ["X", "Y"])
def test_exact_conjugacy_average_all_elements_and_labels(p, axis):
    group = ReesHeisenberg(p)
    for label in range(p):
        for a in group.elements:
            assert group.conjugacy_kernel(axis, label, a) == group.predicted_kernel(axis, label, a)


@pytest.mark.parametrize("p", [3, 5])
def test_nonzero_sectors_identical_but_zero_sector_distinguishes(p):
    group = ReesHeisenberg(p)
    for label in range(1, p):
        for a in group.elements:
            assert group.conjugacy_kernel("X", label, a) == group.conjugacy_kernel("Y", label, a)
    x = (1, 0, 0, 0)
    assert group.conjugacy_kernel("X", 0, x) != group.conjugacy_kernel("Y", 0, x)
    assert group.sector_phase("X", 1, x) == 0
    assert not any(group.conjugacy_kernel("X", 1, x))


def native_sector_density(group, axis, label):
    """Build the actual coset density and central projector, not the formula."""
    elements = group.elements
    index = {a: i for i, a in enumerate(elements)}
    size = len(elements)
    hidden = set(group.hidden(axis))
    rho = np.array([
        [group.mul(group.inv(a), b) in hidden for b in elements]
        for a in elements
    ], dtype=complex) / size
    projector = np.zeros((size, size), dtype=complex)
    for t in range(group.p):
        phase = np.exp(-2j * np.pi * label * t / group.p) / group.p
        for j, a in enumerate(elements):
            projector[index[group.mul(a, (0, 0, 0, t))], j] += phase
    branch = rho @ projector
    assert np.allclose(branch, projector @ rho)
    assert np.isclose(np.trace(branch), 1 / group.p)
    sector = branch * group.p
    assert np.allclose(sector, sector.conj().T)
    assert np.min(np.linalg.eigvalsh(sector)) > -1e-12
    return sector, index


@pytest.mark.parametrize("axis", ["X", "Y"])
@pytest.mark.parametrize("label", [0, 1, 2])
def test_native_density_isometry_compression_and_label_sign(axis, label):
    group = ReesHeisenberg(3)
    rho, index = native_sector_density(group, axis, label)
    elements = group.elements
    size = len(elements)
    cases = [
        ((1, 0, 0, 0), group.identity),
        ((0, 1, 0, 0), group.identity),
        ((0, 0, 0, 1), group.identity),
        (group.identity, (0, 0, 0, 1)),
        ((1, 2, 1, 2), (1, 2, 1, 2)),
        ((1, 2, 1, 2), (2, 0, 1, 1)),
    ]
    for a, b in cases:
        # Direct trace from Theta[(x,y),(x',y')]=rho[x*y^-1,x'*y'^-1]/|G|.
        # No use of the conjugacy compression formula on this side.
        trace = 0j
        for x, y in product(elements, repeat=2):
            g = group.mul(x, group.inv(y))
            gg = group.mul(group.mul(x, a), group.inv(group.mul(y, b)))
            trace += rho[index[g], index[gg]] / size
        word = group.mul(a, group.inv(b))
        expected = evaluate_character(group.conjugacy_kernel(axis, label, word), group.p)
        assert abs(trace - expected) < 1e-11
    for t in range(group.p):
        z = (0, 0, 0, t)
        native_trace = sum(rho[index[g], index[group.mul(g, z)]] for g in elements)
        assert abs(native_trace - np.exp(2j * np.pi * label * t / group.p)) < 1e-11
        # The second central action intertwines with the INVERSE first action.
        for g, y in zip(elements, reversed(elements)):
            x = group.mul(g, y)
            relative = group.mul(x, group.inv(group.mul(y, z)))
            assert relative == group.mul(g, group.inv(z))


@pytest.mark.parametrize("axis", ["X", "Y"])
@pytest.mark.parametrize("label", [0, 1, 2])
def test_control_state_and_equal_translation_falsifier(axis, label):
    group = ReesHeisenberg(3)
    quotient = [(x, y, w, 0) for x, y, w in product(range(3), repeat=3)]
    state = np.array([
        [evaluate_character(group.control_kernel(axis, label, a, group.identity,
                                                 b, group.identity), 3)
         for b in quotient] for a in quotient
    ]) / len(quotient)
    assert np.isclose(np.trace(state), 1)
    assert np.min(np.linalg.eigvalsh(state)) > -1e-12
    if label:
        assert np.allclose(state, np.eye(len(quotient)) / len(quotient))
    else:
        expected = np.array([
            [group.mul(a, group.inv(b))[:3] in {h[:3] for h in group.hidden(axis)}
             for b in quotient] for a in quotient
        ]) / len(quotient)
        assert np.allclose(state, expected)
    # Two equal right translations leave V's image fixed; their successful
    # label cancellation produces an all-ones kernel, not a hidden coset.
    one = (Fraction(1), Fraction(0))
    for a, b in zip(quotient, reversed(quotient)):
        assert group.control_kernel(axis, label, a, a, b, b) == one


@pytest.mark.parametrize("label", [0, 1, 2])
def test_control_word_order_directly_from_native_density(label):
    group = ReesHeisenberg(3)
    rho, index = native_sector_density(group, "X", label)
    a, aa = (1, 0, 0, 0), (0, 1, 0, 0)
    b, bb = (1, 1, 0, 0), (0, 2, 0, 0)
    direct = 0j
    for x, y in product(group.elements, repeat=2):
        xx = group.mul(group.mul(x, a), group.inv(aa))
        yy = group.mul(group.mul(y, b), group.inv(bb))
        g, gg = group.mul(x, group.inv(y)), group.mul(xx, group.inv(yy))
        direct += rho[index[g], index[gg]] / len(group.elements)
    expected = evaluate_character(group.control_kernel("X", label, a, b, aa, bb), 3)
    assert abs(direct - expected) < 1e-11


def test_native_marginals_not_two_right_coset_states():
    group = ReesHeisenberg(3)
    hidden = set(group.hidden("X"))
    size = len(group.elements)
    # At x=1, x'=X the original right-coset matrix entry is 1/|G|,
    # but the conjugation-twirled first marginal has only 1/p of that.
    x, xx = group.identity, (1, 0, 0, 0)
    terms = sum(group.mul(group.mul(y, group.mul(group.inv(x), xx)),
                          group.inv(y)) in hidden for y in group.elements)
    assert Fraction(terms, size**2) == Fraction(1, group.p * size)
    assert Fraction(terms, size**2) != Fraction(1, size)
    # Computational measurement of the second register followed by undoing
    # its known right translation recovers the original native density.
    for y, a, b in zip(group.elements, reversed(group.elements), group.elements[1:]):
        aa, bb = group.mul(a, y), group.mul(b, y)
        recovered = group.mul(group.inv(group.mul(aa, group.inv(y))),
                              group.mul(bb, group.inv(y))) in hidden
        assert recovered == (group.mul(group.inv(a), b) in hidden)


@pytest.mark.parametrize("axis", ["X", "Y"])
@pytest.mark.parametrize("label", [0, 1, 2])
def test_left_action_escape_prevents_global_information_loss_claim(axis, label):
    group = ReesHeisenberg(3)
    rho, index = native_sector_density(group, axis, label)
    s = group.inv((1, 0, 0, 0))
    direct = 0j
    for x, y in product(group.elements, repeat=2):
        g = group.mul(x, group.inv(y))
        # Crucially s*y, NOT y*s: this operation is outside the right algebra.
        gg = group.mul(x, group.inv(group.mul(s, y)))
        direct += rho[index[g], index[gg]] / len(group.elements)
    assert abs(direct - (1 if axis == "X" else 0)) < 1e-11


@pytest.mark.parametrize("p", [3, 5])
def test_actual_two_evaluation_rees_pullback(p):
    group = ReesHeisenberg(p)

    def evaluation(a, s):
        x, y, w, z = a
        return (s * x % p, s * y % p, 0, (s * w + s * s * z) % p)

    generators = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
    for a in group.elements:
        for s, b in product((1, 2), generators):
            assert evaluation(group.mul(a, b), s) == group.mul(evaluation(a, s), evaluation(b, s))
        for axis in ("X", "Y"):
            hidden = set(group.hidden(axis))
            assert all(evaluation(a, s) in hidden for s in (1, 2)) == (a in hidden)


def test_isometry_compression_is_central_operator():
    group = ReesHeisenberg(3)
    elements = group.elements
    index = {a: i for i, a in enumerate(elements)}
    size = len(elements)
    cases = [
        ((1, 0, 0, 0), group.identity),
        ((0, 0, 0, 1), group.identity),
        ((1, 2, 0, 1), (2, 1, 1, 2)),
    ]
    generators = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0)]
    for a, b in cases:
        # Integer numerator of V^*(R_a tensor R_b)V, built from the actual
        # forward isometry, both actions, and the inverse isometry.
        compressed = np.zeros((size, size), dtype=np.int64)
        for g, y in product(elements, repeat=2):
            xx = group.mul(group.mul(g, y), a)
            yy = group.mul(y, b)
            gg = group.mul(xx, group.inv(yy))
            compressed[index[gg], index[g]] += 1
        for s in generators:
            right = np.zeros((size, size), dtype=np.int64)
            for i, g in enumerate(elements):
                right[index[group.mul(g, s)], i] = 1
            assert np.array_equal(right @ compressed, compressed @ right)


@pytest.mark.parametrize("p,cap", [(3, 0), (3, 1), (5, 2), (5, 10), (101, 10)])
def test_probability_bound(p, cap):
    bound = acquisition_bound(p, cap)
    exact = 1 - Fraction(p - 1, p) ** cap
    assert exact <= bound["rare_event_union_bound"]
    assert Fraction(1, 2) <= bound["binary_success_upper_bound"] <= 1
    assert bound["necessary_sources_for_two_thirds"] == (p + 2) // 3
    assert not bound["is_hsp_query_lower_bound"]


def test_large_prime_is_analytic_only():
    p = 2**61 - 1
    bound = acquisition_bound(p, 10**6)
    assert bound["rare_event_union_bound"] == Fraction(10**6, p)
    assert bound["binary_success_upper_bound"] < Fraction(500000000001, 10**12)
    with pytest.raises(ValueError):
        ReesHeisenberg(p)


@pytest.mark.parametrize("p", [True, 2, 9, 37])
def test_reject_invalid_or_unbounded_control_fields(p):
    with pytest.raises(ValueError):
        ReesHeisenberg(p)


@pytest.mark.parametrize("p,cap", [(9, 1), (2, 1), (3, -1), (3, True)])
def test_reject_invalid_resource_inputs(p, cap):
    with pytest.raises(ValueError):
        acquisition_bound(p, cap)
