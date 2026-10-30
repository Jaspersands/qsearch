"""Coupled source/section controls, not a quantum algorithm or speedup test."""
from itertools import product

import numpy as np
import pytest

from theorems.central_character_descent import (
    HeisenbergFixture, check_moment, controlled_discard,
)


@pytest.fixture(scope="module")
def central_quotient():
    # UT3(F_3) x F_3; H={(a,0,c,c)} is nonnormal and meets the
    # two-dimensional center in a one-dimensional diagonal subgroup.
    base = HeisenbergFixture(3)
    elements = tuple(product(range(3), repeat=4))
    index = {g: i for i, g in enumerate(elements)}
    hidden = {(a, 0, c, c) for a, c in product(range(3), repeat=2)}
    center = {(0, 0, z, t) for z, t in product(range(3), repeat=2)}

    def mul(a, b):
        return (*base.multiply(a[:3], b[:3]), (a[3] + b[3]) % 3)

    def inv(a):
        return (*base.inverse(a[:3]), -a[3] % 3)

    def dilate(a, s):
        return (*base.dilate(a[:3], s), s * s * a[3] % 3)

    def right(g):
        return np.array([index[mul(x, inv(g))] for x in elements])

    rho = np.array([[int(mul(inv(x), y) in hidden) / 81 for y in elements]
                    for x in elements], dtype=complex)
    branches, projectors = {}, {}
    for label in product(range(3), repeat=2):
        projector = np.zeros((81, 81), dtype=complex)
        for z, t in product(range(3), repeat=2):
            projector[right((0, 0, z, t)), np.arange(81)] += (
                np.exp(-2j * np.pi * (label[0] * z + label[1] * t) / 3) / 9
            )
        projectors[label] = projector
        branches[label] = projector @ rho @ projector.conj().T

    return elements, hidden, center, mul, inv, dilate, right, rho, branches, projectors


def test_zero_branches_vanish_and_nonzero_trace_includes_intersection(central_quotient):
    elements, hidden, center, mul, inv, dilate, _, rho, branches, projectors = central_quotient
    assert len(hidden & center) == 3
    assert any(mul(mul(g, h), inv(g)) not in hidden for g in elements for h in hidden)
    assert all(dilate(h, s) in hidden for h in hidden for s in (1, 2))
    np.testing.assert_allclose(sum(projectors.values()), np.eye(81), atol=1e-12)
    np.testing.assert_allclose(sum(branches.values()), rho, atol=1e-12)
    for label, branch in branches.items():
        if sum(label) % 3:
            np.testing.assert_allclose(branch, 0, atol=1e-12)
        else:
            assert np.trace(branch) == pytest.approx(1 / 3)
            assert np.linalg.eigvalsh(branch).min() > -1e-12


@pytest.mark.parametrize("nonlinear", [False, True])
def test_actual_quotient_output_and_wrong_normalization_countercontrol(central_quotient, nonlinear):
    _, _, _, mul, _, dilate, right, _, branches, _ = central_quotient
    quotient = tuple(product(range(3), repeat=2))

    def section(q):
        x, y = q
        return (x, y, (x * y + y * y) % 3, (x * x + y) % 3) if nonlinear else (x, y, 0, 0)

    assert all(section(q)[:2] == q for q in quotient)
    assert any(mul(section(q), section(r)) != section(tuple((a + b) % 3 for a, b in zip(q, r)))
               for q in quotient for r in quotient)
    expected = np.array([[int(q[1] == r[1]) / 9 for r in quotient] for q in quotient])
    for a in range(3):
        labels = ((a, -a % 3), (-a % 3, a))
        scales = (1, 2)
        assert check_moment(labels, scales, 3, 2) == (0, 1)
        output = np.ones((9, 9), dtype=complex) / 9
        wrong = output.copy()
        for label, scale in zip(labels, scales):
            controls = np.array([right(dilate(section(q), scale)) for q in quotient])
            branch = branches[label]
            output *= 9 * controlled_discard(branch / np.trace(branch), controls)
            # The old transverse formula divides by 1/|Z| instead of |H cap Z|/|Z|.
            wrong *= 9 * controlled_discard(9 * branch, controls)
        np.testing.assert_allclose(output, expected, atol=1e-12)
        assert np.trace(output) == pytest.approx(1)
        assert np.trace(wrong) == pytest.approx(9)


def test_trivial_base_character_is_not_a_complete_linear_label_instrument(central_quotient):
    _, _, _, _, _, _, _, _, branches, projectors = central_quotient
    # With chi=1, all nine linear labels give the same projector. Individual
    # branch identities remain valid, but these are not nine physical outcomes.
    assert np.linalg.norm(9 * projectors[(0, 0)] - np.eye(81)) > 1
    assert 9 * np.trace(branches[(0, 0)]) == pytest.approx(3)


def _five_label_witness(labels):
    """Bounded F_3^2 control, not the asymptotic SDE solver."""
    reachable = {(0, 0): ()}
    for i, label in enumerate(labels):
        for partial, indices in tuple(reachable.items()):
            total = tuple((x + y) % 3 for x, y in zip(partial, label))
            selected = (*indices, i)
            if total == (0, 0):
                scales = [0] * len(labels)
                for j in selected:
                    scales[j] = 1
                scales[selected[0]] = 2
                return tuple(scales)
            reachable.setdefault(total, selected)
    raise AssertionError("five F_3^2 labels must have a nonempty zero-sum subset")


def test_all_measured_records_include_inactive_and_impossible_branches(central_quotient):
    _, _, _, _, _, dilate, right, _, branches, _ = central_quotient
    quotient = tuple(product(range(3), repeat=2))
    expected = np.array([[int(q[1] == r[1]) / 9 for r in quotient] for q in quotient])
    labels = tuple(branches)
    moments = {}
    masses = {label: np.trace(branches[label]) for label in labels}
    for label in labels:
        for scale in (0, 1, 2):
            controls = np.array([
                right(dilate((x, y, 0, 0), scale)) if scale else np.arange(81)
                for x, y in quotient
            ])
            moments[label, scale] = 9 * controlled_discard(branches[label], controls)

    total = np.zeros((9, 9), dtype=complex)
    record_count = positive_count = 0
    largest_error = 0.0
    for record in product(labels, repeat=5):
        scales = _five_label_witness(record)
        assert any(scales)
        assert all(sum(s * s * label[j] for label, s in zip(record, scales)) % 3 == 0
                   for j in range(2))
        output = np.ones((9, 9), dtype=complex) / 9
        for label, scale in zip(record, scales):
            output *= moments[label, scale]
        mass = np.prod([masses[label] for label in record])
        largest_error = max(largest_error, float(np.max(np.abs(output - mass * expected))))
        total += output
        record_count += 1
        positive_count += all(sum(label) % 3 == 0 for label in record)
    assert record_count == 9**5 and positive_count == 3**5
    assert largest_error < 1e-12
    np.testing.assert_allclose(total, expected, atol=1e-12)
    assert np.trace(total) == pytest.approx(1)


def test_dropping_inactive_masses_or_accepting_zero_witness_is_wrong(central_quotient):
    _, _, _, _, _, dilate, right, _, branches, _ = central_quotient
    quotient = tuple(product(range(3), repeat=2))
    branch = branches[(0, 0)]
    mass = np.trace(branch)
    active_controls = np.array([right(dilate((x, y, 0, 0), 2)) for x, y in quotient])
    active_only = controlled_discard(branch, active_controls)
    all_five = mass**4 * active_only
    assert np.trace(active_only) == pytest.approx(81 * np.trace(all_five))

    idle_controls = np.tile(np.arange(81), (9, 1))
    idle_output = controlled_discard(branch / mass, idle_controls)
    expected = np.array([[int(q[1] == r[1]) / 9 for r in quotient] for q in quotient])
    np.testing.assert_allclose(idle_output, np.ones((9, 9)) / 9, atol=1e-12)
    assert np.linalg.norm(idle_output - expected) > 0.5
