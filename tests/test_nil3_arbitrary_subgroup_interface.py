"""Exact finite controls for the written arbitrary-H reduction, not a solver.

Hidden bases/potentials occur only in truth fixtures. No enumeration below
is claimed to be efficient in log|G| or exposed as a physical controller.
"""

from itertools import product
from math import sqrt

import numpy as np
import pytest

from theorems.affine_phase_channel_audit import coset_mixture, points, span
from theorems.nil3_cocycle_receiver import ClassThreeBCH, graph_branches


@pytest.fixture(scope="module")
def group():
    # X,Y,E,Z,A; [X,Y]=Z, [X,Z]=A, [Y,E]=A. E is NOT a central factor.
    return ClassThreeBCH(5, 3, 2, {
        (0, 1): (0, 0, 0, 1, 0),
        (0, 3): (0, 0, 0, 0, 1),
        (1, 2): (0, 0, 0, 0, 1),
    })


@pytest.fixture(scope="module")
def transverse(group):
    # Two independent quotient directions with genuinely hidden normal lifts.
    # The quotient lifts do not commute: their central bracket is cancelled
    # by the hidden Z components.
    basis = [(1, 1, 0, 1, 2), (0, 0, 1, 4, 4)]
    hidden = span(group.p, group.dimension, basis)
    quotient_basis = [h[:group.m] for h in basis]
    return basis, hidden, quotient_basis


def _hidden_log(q):
    x, y, e = q
    assert y == x
    return (x, x, e, (x-e) % 5, (2*x + 4*e) % 5)


def _potential(group, q, gauge=0):
    x, y, e = q
    projected_x = (x + gauge*(y-x)) % group.p
    u = (projected_x, projected_x, (e + 2*gauge*(y-x)) % group.p)
    r = group.add(q, group.scale(-1, u))
    _, normal = group.to_chart(_hidden_log(u))
    return group.add(group.action(r, normal), group.cocycle(r, u))


@pytest.mark.parametrize("gauge", [0, 1, 3])
def test_potential_has_explicit_total_degree_at_most_three(group, gauge):
    for q in points(5, 3):
        x, y, e = q
        px = (x + gauge*(y-x)) % 5
        u = (px, px, (e + 2*gauge*(y-x)) % 5)
        qlog, ulog = group.lift(q), group.lift(u)
        a = group.ideal(_hidden_log(u)[3:])
        qu = group.bracket(qlog, ulog)
        expanded = group.add(
            a, group.bracket(qlog, a),
            group.scale(-pow(2, -1, 5), group.bracket(ulog, a)),
            group.scale(pow(2, -1, 5), qu),
            group.scale(pow(3, -1, 5), group.bracket(qlog, qu)),
            group.scale(-pow(6, -1, 5), group.bracket(ulog, qu)),
        )
        assert expanded[:3] == (0, 0, 0)
        assert expanded[3:] == _potential(group, q, gauge)


def _mixed_blocks(group, hidden):
    """Construct actual rho_H from right multiplication, not the potential."""
    assert group.p**group.dimension <= 4000
    quotient = points(group.p, group.m)
    index = {q: i for i, q in enumerate(quotient)}
    counts = np.zeros((len(quotient), len(quotient)) + (group.p,) * group.n,
                      dtype=np.int64)
    for g in product(range(group.p), repeat=group.dimension):
        q, a = group.to_chart(g)
        for h in hidden:
            r, b = group.to_chart(group.bch(g, h))
            difference = tuple((x-y) % group.p for x, y in zip(a, b))
            counts[(index[q], index[r]) + difference] += 1
    transformed = np.fft.ifftn(counts, axes=tuple(range(2, 2+group.n)))
    transformed /= group.p**group.dimension
    return {label: transformed[(slice(None), slice(None)) + label]
            for label in product(range(group.p), repeat=group.n)}


def test_rank_two_hidden_subgroup_is_transverse_and_abelian(group, transverse):
    _, hidden, quotient_basis = transverse
    assert len(hidden) == 25
    assert len(span(5, 3, quotient_basis)) == 25
    assert {h for h in hidden if not any(h[:3])} == {group.zero}
    for h in hidden:
        for k in hidden:
            assert group.bracket(h, k) == group.zero
            assert group.bch(h, k) == group.add(h, k) in hidden
    x, y, e, z, a = [
        tuple(int(i == j) for i in range(5)) for j in range(5)
    ]
    assert group.bracket(y, e) == a
    assert group.bracket(x, group.bracket(x, y)) == a != group.zero
    assert group.bracket(x, y) == z
    assert group.bracket(group.lift(quotient_basis[0]),
                         group.lift(quotient_basis[1])) != group.zero


@pytest.mark.parametrize("gauge", [0, 1, 3])
def test_common_cubic_potential_increment_for_all_hidden_directions(
    group, transverse, gauge,
):
    _, hidden, _ = transverse
    for q in points(5, 3):
        for h in hidden:
            u, normal = group.to_chart(h)
            difference = group.add(_potential(group, group.add(q, u), gauge),
                                   group.scale(-1, _potential(group, q, gauge)))
            assert difference == group.add(group.action(q, normal),
                                           group.cocycle(q, u))


def test_projection_gauge_changes_no_within_coset_phase(group, transverse):
    _, hidden, _ = transverse

    def difference(q):
        return group.add(_potential(group, q, 1),
                         group.scale(-1, _potential(group, q, 0)))

    assert any(any(difference(q)) for q in points(5, 3))
    for q in points(5, 3):
        for h in hidden:
            assert difference(group.add(q, h[:3])) == difference(q)


def test_noncommuting_linear_graph_is_not_a_hidden_subgroup(group):
    x, y = (1, 0, 0, 0, 0), (0, 1, 0, 0, 0)
    invalid_graph = span(5, 5, [x, y])
    assert group.bracket(x, y) != group.zero
    assert group.bch(x, y) not in invalid_graph
    # Taking pi=id and a=0 would make the potential identically zero,
    # but its required increment is this nonzero cocycle.
    assert group.cocycle(x[:3], y[:3]) != (0, 0)


def test_quadratic_truncation_fails_for_valid_rank_two_hidden_subgroup(group):
    def truncated(q):
        u = (q[0], q[0], q[2])
        qlog, ulog = group.lift(q), group.lift(u)
        qu = group.bracket(qlog, ulog)
        cubic = group.add(
            group.scale(pow(3, -1, 5), group.bracket(qlog, qu)),
            group.scale(-pow(6, -1, 5), group.bracket(ulog, qu)),
        )[3:]
        return group.add(_potential(group, q), group.scale(-1, cubic))

    q, v = (0, 1, 0), (1, 1, 0)
    _, normal = group.to_chart(_hidden_log(v))
    expected = group.add(group.action(q, normal), group.cocycle(q, v))
    actual = group.add(truncated(group.add(q, v)), group.scale(-1, truncated(q)))
    full = group.add(_potential(group, group.add(q, v)),
                     group.scale(-1, _potential(group, q)))
    assert full == expected
    assert actual != expected
    assert group.add(full, group.scale(-1, actual)) == (0, 4)


def test_actual_rank_two_mixed_source_has_every_uniform_fourier_label(
    group, transverse,
):
    _, hidden, quotient_basis = transverse
    blocks = _mixed_blocks(group, hidden)
    potentials = [_potential(group, q) for q in points(5, 3)]
    assert len(blocks) == 25  # Includes zero; no character postselection.
    for label, block in blocks.items():
        probability = np.trace(block).real
        assert probability == pytest.approx(1/25)
        phases = [sum(a*b for a, b in zip(label, value)) % 5
                  for value in potentials]
        expected = coset_mixture(5, 3, quotient_basis, phases)
        assert np.max(abs(block / probability - expected)) < 1e-12
    # Nonzero phases actually occur, so a phase-free implementation fails.
    assert np.max(abs(blocks[(0, 1)] - blocks[(0, 0)])) > 1e-4


def test_normal_measurement_needs_twist_correction_and_keeps_full_intersection(group):
    # H=<Y+E,Z>. K=H intersect N=<Z> is normal in H but NOT in G.
    hidden = span(5, 5, [(0, 1, 1, 0, 0), (0, 0, 0, 1, 0)])
    normal_hidden = {(h[3], h[4]) for h in hidden if not any(h[:3])}
    assert normal_hidden == {(t, 0) for t in range(5)}
    saw_wrong_uncorrected_span = False
    for x, y, e in points(5, 3):
        representative = (x, y, e, 2, 3)
        branches = {}
        for h in hidden:
            q, normal = group.to_chart(group.bch(representative, h))
            branches.setdefault(q, set()).add(normal)
        assert len(branches) == 5
        for q, values in branches.items():
            anchor = next(iter(values))
            differences = {group.add(v, group.scale(-1, anchor)) for v in values}
            saw_wrong_uncorrected_span |= differences != normal_hidden
            corrected = {group.action(group.scale(-1, q), v) for v in values}
            anchor = next(iter(corrected))
            assert {group.add(v, group.scale(-1, anchor)) for v in corrected} == normal_hidden
    assert saw_wrong_uncorrected_span


def test_nontransverse_source_does_not_have_uniform_character_labels(group):
    hidden = span(5, 5, [(0, 1, 1, 0, 0), (0, 0, 0, 1, 0)])
    blocks = _mixed_blocks(group, hidden)
    probabilities = {label: np.trace(block).real for label, block in blocks.items()}
    assert sum(probabilities.values()) == pytest.approx(1)
    assert probabilities[(0, 0)] == pytest.approx(1/5)
    assert probabilities[(1, 0)] == pytest.approx(0)
    assert probabilities[(0, 1)] == pytest.approx(1/25)
    assert probabilities[(0, 0)] != pytest.approx(1/25)


def test_intersection_normalizer_retains_h_and_quotient_is_transverse(group):
    hidden = span(5, 5, [(0, 1, 1, 0, 0), (0, 0, 0, 1, 0)])
    known = span(5, 5, [(0, 0, 0, 1, 0)])
    z = (0, 0, 0, 1, 0)
    normalizer = set()
    for g in product(range(5), repeat=5):
        lie_test = group.bracket(g, z) in known
        conjugate = group.bch(group.bch(group.scale(-1, g), z), g)
        assert lie_test == (conjugate in known)
        if lie_test:
            normalizer.add(g)
    assert len(normalizer) == 625 < 3125
    assert hidden <= normalizer
    assert any(group.bracket(group.lift(q), z) not in known for q in points(5, 3))

    # In M/K the coordinates Y,E,A remain; [Y,E]=A.
    def quotient(g):
        assert g in normalizer
        return (g[1], g[2], g[4])

    image = {quotient(h) for h in hidden}
    normal_image = {quotient(g) for g in normalizer if not any(g[:3])}
    assert len(image) == 5
    assert image & normal_image == {(0, 0, 0)}
    assert len(normal_image) == 5


def test_oracle_membership_certifies_an_intersection_superset(group):
    hidden = span(5, 5, [(0, 1, 1, 0, 0), (0, 0, 0, 1, 0)])
    normal_basis = [(0, 0, 0, 1, 0), (0, 0, 0, 0, 1)]
    intersection = hidden & span(5, 5, normal_basis)

    def oracle(g):
        return min(group.bch(g, h) for h in hidden)

    identity_label = oracle(group.zero)
    for proposed_basis in [normal_basis[:1], normal_basis]:
        estimate = span(5, 5, proposed_basis)
        assert intersection <= estimate  # Exact Fourier samples guarantee this.
        accepted = all(oracle(k) == identity_label for k in proposed_basis)
        assert accepted == (estimate == intersection)

    # Membership alone cannot certify an underestimate. The inclusion above
    # is indispensable, including when accounting for approximate QFT error.
    underestimate = {group.zero}
    assert underestimate < intersection
    assert oracle(group.zero) == identity_label


def _checked_transverse_candidate(group, evaluator, estimated_image, generators):
    """Test-only public predicate; does not receive the true hidden subgroup."""
    identity_label = evaluator(group.zero)
    return (all(evaluator(g) == identity_label for g in generators) and
            span(group.p, group.m, [g[:group.m] for g in generators]) == estimated_image)


def test_checked_final_output_rejects_overestimated_support_and_bad_lifts(group, transverse):
    basis, hidden, quotient_basis = transverse

    def evaluator(g):
        return min(group.bch(g, h) for h in hidden)

    actual_image = span(5, 3, quotient_basis)
    full_image = set(points(5, 3))
    assert actual_image < full_image
    assert _checked_transverse_candidate(group, evaluator, actual_image, basis)
    assert not _checked_transverse_candidate(group, evaluator, full_image, basis)
    outside = (1, 0, 0, 0, 0)
    assert span(5, 3, quotient_basis + [outside[:3]]) == full_image
    assert not _checked_transverse_candidate(group, evaluator, full_image, basis + [outside])
    wrong_normal_lift = group.add(basis[0], (0, 0, 0, 0, 1))
    assert wrong_normal_lift[:3] == basis[0][:3]
    assert not _checked_transverse_candidate(
        group, evaluator, actual_image, [wrong_normal_lift, basis[1]])


def test_membership_alone_does_not_replace_projected_span_check(group, transverse):
    basis, hidden, quotient_basis = transverse

    def evaluator(g):
        return min(group.bch(g, h) for h in hidden)

    redundant = [basis[0], group.scale(2, basis[0]), group.zero]
    assert all(evaluator(g) == evaluator(group.zero) for g in redundant)
    assert not _checked_transverse_candidate(
        group, evaluator, span(5, 3, quotient_basis), redundant)


def test_false_frequency_can_make_an_incomplete_output_pass_public_checks(group, transverse):
    basis, hidden, quotient_basis = transverse

    def evaluator(g):
        return min(group.bch(g, h) for h in hidden)

    true_image = span(5, 3, quotient_basis)
    exact_frequency, leaked_frequency = (1, 4, 0), (0, 0, 1)
    assert all(sum(x*y for x, y in zip(u, exact_frequency)) % 5 == 0 for u in true_image)
    assert any(sum(x*y for x, y in zip(u, leaked_frequency)) % 5 != 0 for u in true_image)
    estimate = {u for u in points(5, 3) if all(
        sum(x*y for x, y in zip(u, frequency)) % 5 == 0
        for frequency in (exact_frequency, leaked_frequency))}
    assert estimate < true_image
    assert _checked_transverse_candidate(group, evaluator, estimate, [basis[0]])
    assert span(5, 5, [basis[0]]) < hidden
    # The check is not an unconditional certificate against QFT leakage.


def test_full_output_must_retain_the_verified_normal_intersection(group):
    lift, normal_generator = (0, 1, 1, 0, 0), (0, 0, 0, 1, 0)
    hidden = span(5, 5, [lift, normal_generator])
    missing_intersection = span(5, 5, [lift])

    def evaluator(g):
        return min(group.bch(g, h) for h in hidden)

    # Projection M -> (M/K)/[M/K,M/K] in the earlier nonnormal-K fixture.
    projection = lambda g: (g[1], g[2])
    assert {projection(g) for g in missing_intersection} == {projection(g) for g in hidden}
    assert evaluator(lift) == evaluator(group.zero)
    assert missing_intersection < hidden
    restored = span(5, 5, [lift, normal_generator])
    assert restored == hidden
    assert group.bracket(lift, normal_generator) == group.zero


def test_checked_zero_support_outputs_no_transverse_generators(group):
    identity_evaluator = lambda g: g
    assert _checked_transverse_candidate(group, identity_evaluator, {(0, 0, 0)}, [])
    assert not _checked_transverse_candidate(
        group, identity_evaluator, {(0, 0, 0)}, [(0, 0, 0, 1, 0)])


def test_learning_the_whole_quotient_image_reduces_ambient_class(group, transverse):
    _, hidden, quotient_basis = transverse
    image = span(5, 3, quotient_basis)
    preimage = {g for g in product(range(5), repeat=5) if g[:3] in image}
    normal = span(5, 5, [(0, 0, 0, 1, 0), (0, 0, 0, 0, 1)])
    assert preimage == {group.bch(h, n) for h in hidden for n in normal}
    assert len(preimage) == 625
    basis = [(1, 1, 0, 0, 0), (0, 0, 1, 0, 0),
             (0, 0, 0, 1, 0), (0, 0, 0, 0, 1)]
    assert any(any(group.bracket(a, b)) for a in basis for b in basis)
    assert all(group.bracket(a, group.bracket(b, c)) == group.zero
               for a in basis for b in basis for c in basis)

    # Skipping transversality is invalid: H=G has full U but remains class 3.
    x, y = (1, 0, 0, 0, 0), (0, 1, 0, 0, 0)
    assert group.bracket(x, group.bracket(x, y)) != group.zero


def test_public_class_two_stop_can_precede_exact_support_recovery(group):
    hidden_line = span(5, 5, [(1, 1, 0, 1, 2)])
    actual_image = {h[:3] for h in hidden_line}
    observed_frequency = (1, 4, 0)
    estimated_image = {q for q in points(5, 3)
                       if sum(a*b for a, b in zip(q, observed_frequency)) % 5 == 0}
    assert actual_image < estimated_image
    assert len(actual_image) == 5 and len(estimated_image) == 25
    preimage = {g for g in product(range(5), repeat=5) if g[:3] in estimated_image}
    assert hidden_line <= preimage
    public_basis = [(1, 1, 0, 0, 0), (0, 0, 1, 0, 0),
                    (0, 0, 0, 1, 0), (0, 0, 0, 0, 1)]
    assert all(group.bracket(a, group.bracket(b, c)) == group.zero
               for a in public_basis for b in public_basis for c in public_basis)
    # This is a valid nil-2 oracle restriction even though U was not learned.
    assert group.bch((1, 1, 0, 0, 0), (0, 0, 1, 0, 0)) in preimage


@pytest.mark.parametrize("direction", [(1, 1, 0), (0, 0, 1), (1, 1, 2)])
def test_known_line_inside_learned_subspace_retains_quadratic_graph(group, transverse, direction):
    _, hidden, _ = transverse
    representative = (2, 3, 4, 1, 2)
    source = {group.bch(representative, h): 1/sqrt(len(hidden)) for h in hidden}
    branches = graph_branches(group, source, direction)
    assert len(branches) == 5
    generator = _hidden_log(direction)
    for values in branches.values():
        assert len(values) == 5
        assert sum(abs(a)**2 for a in values.values()) == pytest.approx(1/5)
        by_t = {key[0]: key[1:] for key in values}
        assert set(by_t) == set(range(5))
        offset = by_t[0]
        for t in range(5):
            _, expected = group.to_chart(group.scale(t, generator))
            assert by_t[t] == group.add(offset, expected)


@pytest.mark.parametrize("basis", [[], [(1, 0, 0)], [(1, 0, 0), (0, 0, 1)],
                                  [(1, 0, 0), (0, 1, 0), (0, 0, 1)]])
def test_phase_free_fourier_sampling_is_not_a_line_only_interface(basis):
    ambient = points(5, 3)
    source = coset_mixture(5, 3, basis, [0]*125)
    transform = np.array([
        [np.exp(-2j*np.pi*sum(a*b for a, b in zip(x, y))/5)/sqrt(125)
         for x in ambient] for y in ambient
    ])
    probability = np.diag(transform @ source @ transform.conj().T).real
    annihilator = {y for y in ambient if all(
        sum(a*b for a, b in zip(y, v)) % 5 == 0 for v in basis)}
    assert len(annihilator) == 5**(3-len(basis))
    for y, value in zip(ambient, probability):
        assert value == pytest.approx(1/len(annihilator) if y in annihilator else 0)
